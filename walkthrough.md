# Walkthrough: Multi-Candidate Ranking & Shortlisting

RecruitFlow AI now supports batch processing of multiple resumes, delivering a ranked shortlist with deep-dive candidate evaluations — all within the premium ChatGPT-style interface.

## 🚀 New Features

### 1. Batch Resume Processing
- **Multi-Upload support**: You can now select and upload multiple PDF resumes simultaneously.
- **Dynamic File Chips**: The UI displays each attached file with an option to remove individual resumes before processing.
- **Parallel Pipeline**: The backend extracts text from all provided PDFs and processes them through the multi-agent pipeline.

### 2. Multi-Agent Ranking Pipeline (LangGraph)
We've refined the explicit agent boundaries for batch processing:
- **JD Parser**: Extracts requirements from your job description.
- **Candidate Screener**: Individually evaluates each resume against the JD, generating scores and technical interview questions.
- **Ranking Agent**: Consolidates all evaluations, sorts candidates by match percentage, and provides a comparative summary.

### 3. Rank-Driven Chat Interface
- **Shortlist Summary**: The response starts with an AI-generated summary of the candidate pool.
- **Interactive List**: Candidates are displayed in order of rank. Clicking a candidate expands their specific experience details, strengths, and interview strategy.
- **Persistent Batch History**: History items now track the top candidate of the batch, preserving the entire ranked shortlist for future review.

### 4. Fully Dockerized Connectivity
- **Nginx Reverse Proxy**: A custom Nginx configuration now handles frontend delivery and proxies API calls to the backend, ensuring seamless communication in containerized environments.
- **Deployment Ready**: Standardized Docker configurations allow for one-click deployment to public cloud providers.

## 🛠️ Technical Implementation

### Core Components
- **LangGraph**: Orchestrates the 3-stage pipeline (`jd_parser` -> `candidate_screener` -> `ranking_agent`).
- **FastAPI**: Updated to handle `List[UploadFile]` and map-reduce style extraction.
- **AgentOps**: Every batch run is instrumented, showing the nested tool calls for each candidate.

---

## 📺 Demo Preparation

To test the new features:
1. Ensure your `.env` has active keys.
2. Run `docker-compose up --build`.
3. Open `http://localhost:8080`.
4. Upload **3 different resumes** and a Job Description.
5. Watch the **Ranking Agent** produce the final shortlist.

> [!IMPORTANT]
> **Deployment**: Review the [deployment_guide.md](file:///c:/Users/atsha/Downloads/recruitment_automation/deployment_guide.md) to move your RecruitFlow instance to the public web.
