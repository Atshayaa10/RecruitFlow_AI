import os
from typing import TypedDict, List, Annotated, Optional
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

# Initialize Groq LLM
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name=MODEL_NAME)

# --- State Definition ---
class CandidateState(BaseModel):
    name: str
    filename: str
    resume_text: str
    parsed_resume: Optional[dict] = None
    score_report: Optional[dict] = None
    recommendation: Optional[str] = None

class AgentState(TypedDict):
    job_description: str
    resumes: List[dict] # List of {"filename": str, "text": str}
    parsed_jd: Optional[dict]
    candidates: List[dict]
    ranked_shortlist: Optional[dict]
    messages: List[BaseMessage]

# --- Structured Output Schemas ---
class JDStructure(BaseModel):
    title: str = Field(description="Job title")
    skills: List[str] = Field(description="Key technical and soft skills required")
    experience_years: str = Field(description="Minimum years of experience required (as a string, e.g., '5')")
    responsibilities: List[str] = Field(description="Top responsibilities")

class ResumeStructure(BaseModel):
    name: str = Field(description="Candidate full name")
    experience_years: str = Field(description="Total years of experience (as a string, e.g., '3')")
    skills: List[str] = Field(description="Top skills mentioned")
    education: str = Field(description="Highest degree or institution")

class ScoreReport(BaseModel):
    match_percentage: float = Field(description="Match percentage (0-100)")
    reasoning: str = Field(description="Step-by-step reasoning for the score based on skills, experience, and education")
    strengths: List[str] = Field(description="Alignment with the JD")
    gaps: List[str] = Field(description="Missing skills or experience gaps")
    qualified: bool = Field(description="Whether the candidate is considered qualified")

class RankedCandidate(BaseModel):
    name: str
    filename: str
    rank: int
    score: float
    reason: str

class RankedShortlist(BaseModel):
    top_candidates: List[RankedCandidate]
    summary: str = Field(description="Overall summary of the candidate pool")

# --- Agent Nodes ---

def jd_parser_node(state: AgentState):
    """Extracts structured data from the job description."""
    print("Agent: JDParser is analyzing the job description...")
    prompt = f"Analyze this Job Description and extract structured details:\n\n{state['job_description']}"
    structured_llm = llm.with_structured_output(JDStructure)
    result = structured_llm.invoke(prompt)
    return {"parsed_jd": result.dict()}

def candidate_screener_node(state: AgentState):
    """Parses and scores each candidate individually."""
    print(f"Agent: CandidateScreener is processing {len(state['resumes'])} candidates...")
    candidates = []
    
    resume_parser_llm = llm.with_structured_output(ResumeStructure)
    scoring_llm = llm.with_structured_output(ScoreReport)
    
    for res in state['resumes']:
        filename = res['filename']
        text = res['text']
        print(f"  - Screening {filename}...")
        
        # 1. Parse Resume
        parse_result = resume_parser_llm.invoke(f"Extract details from this resume:\n\n{text}")
        
        # 2. Score against JD with Rubric
        score_prompt = f"""
        Strictly evaluate this Candidate against the Job Description using this 100-point rubric:
        1. Core Skills (50 pts): Match of specific tech stack (languages, frameworks).
        2. Experience (30 pts): Seniority and responsibility alignment. 
        3. Education & Certs (20 pts): Minimum requirements met.
        
        Provide the reasoning first, then the final match_percentage. DO NOT use generic or rounded numbers like 60 or 40 unless exactly earned.
        
        JD: {state['parsed_jd']}
        Candidate: {parse_result.dict()}
        """
        score_result = scoring_llm.invoke(score_prompt)
        
        # 3. Get Interview Recommendation
        match_score = score_result.match_percentage
        rec_prompt = f"""
        Based on this match score {match_score}%, provide 2 specific technical interview questions for this candidate.
        MANDATORY: Use a numbered list format (1. Question...)
        """
        rec_response = llm.invoke(rec_prompt)
        
        # Safe extraction of years for display
        def safe_int(val):
            try: return int(float(str(val)))
            except: return 0

        candidates.append({
            "name": parse_result.name,
            "filename": filename,
            "resume_text": text,
            "parsed_resume": {**parse_result.dict(), "experience_years": safe_int(parse_result.experience_years)},
            "score_report": score_result.dict(),
            "recommendation": rec_response.content
        })
        
    return {"candidates": candidates}

def ranking_agent_node(state: AgentState):
    """Compares all evaluated candidates and ranks them."""
    print("Agent: RankingAgent is producing the final shortlist...")
    
    candidate_summaries = []
    for c in state['candidates']:
        # c is now a dict
        candidate_summaries.append({
            "name": c['name'],
            "filename": c['filename'],
            "score": c['score_report']['match_percentage'],
            "skills": c['parsed_resume']['skills']
        })
        
    prompt = f"""
    Rank these candidates for the following Job Description.
    
    JD: {state['parsed_jd']}
    Candidates: {candidate_summaries}
    
    Return a ranked list with specific reasons for their rank.
    """
    structured_llm = llm.with_structured_output(RankedShortlist)
    result = structured_llm.invoke(prompt)
    return {"ranked_shortlist": result.dict()}

# --- Graph Construction ---

def build_graph():
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("jd_parser", jd_parser_node)
    workflow.add_node("candidate_screener", candidate_screener_node)
    workflow.add_node("ranking_agent", ranking_agent_node)

    # Set Edges
    workflow.set_entry_point("jd_parser")
    workflow.add_edge("jd_parser", "candidate_screener")
    workflow.add_edge("candidate_screener", "ranking_agent")
    workflow.add_edge("ranking_agent", END)

    return workflow.compile()

# Execution interface
recruitment_pipeline = build_graph()
