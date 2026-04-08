import sys
import logging

# Silence AgentOps logging to prevent the emoji-induced crash during init on Windows
# (Charmap cannot encode the 'Thinking Face' emoji AgentOps uses in logs)
logging.getLogger("agentops").setLevel(logging.ERROR)

# Comprehensive UTF-8 wrap for Windows to prevent other emoji-logging crashes
# if sys.platform == "win32":
#     import codecs
#     if hasattr(sys.stdout, 'detach'):
#         sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
#     if hasattr(sys.stderr, 'detach'):
#         sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

import os
import agentops
import time
from dotenv import load_dotenv
from typing import TypedDict, List, Annotated, Optional
from datetime import datetime

# Initialize AgentOps at the very beginning
load_dotenv()
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")

# Nuclear Stabilization: Disable all magic/automatic instrumentors to stop circular import crashes.
# We will rely on our manual decorators (@agentops.track_tool) in agents.py.
if AGENTOPS_API_KEY:
    agentops.init(api_key=AGENTOPS_API_KEY, default_tags=["recruitment-automation"], instrument_llm_calls=False)

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import uvicorn
import traceback

# --- Imports and AgentOps Init ---
from agents import recruitment_pipeline
from utils import extract_text_from_pdf
from database import init_db, save_analysis, get_history, get_analysis_detail
from fastapi.responses import FileResponse, HTMLResponse
import os

# Initialize DB on startup
init_db()

app = FastAPI(title="RecruitFlow AI API")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_msg = f"CRITICAL ERROR: {exc}\n{traceback.format_exc()}"
    with open("debug_backend.log", "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now()}] {error_msg}\n")
    print(error_msg)
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": str(exc)},
    )

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to frontend
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
if not os.path.exists(FRONTEND_DIR):
    # Fallback for Docker environment where frontend might be at /app/frontend
    FRONTEND_DIR = "/app/frontend"

@app.get("/", response_class=HTMLResponse)
def read_root():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return "RecruitFlow AI API is running. Frontend not found."

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# History endpoints
@app.get("/history")
async def fetch_history(user_id: str = "default_user"):
    return {"status": "success", "data": get_history(user_id)}

@app.get("/history/{analysis_id}")
async def fetch_detail(analysis_id: int):
    detail = get_analysis_detail(analysis_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return {"status": "success", "data": detail}

class JobDescription(BaseModel):
    jd_text: str

@app.post("/analyze")
async def analyze_recruitment(
    jd_text: str = Form(...),
    resume_files: List[UploadFile] = File(...)
):
    with open("debug_backend.log", "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now()}] Received request with {len(resume_files)} files\n")
    try:
        resumes_data = []
        for resume_file in resume_files:
            print(f"DEBUG: Extracting text from PDF: {resume_file.filename}...")
            resume_bytes = await resume_file.read()
            resume_text = extract_text_from_pdf(resume_bytes)
            
            if resume_text:
                resumes_data.append({
                    "filename": resume_file.filename,
                    "text": resume_text
                })
            else:
                print(f"WARNING: Could not extract text from {resume_file.filename}")

        if not resumes_data:
            raise HTTPException(status_code=400, detail="Could not extract text from any provided PDF Resumes")

        # Prepare state for the recruitment graph
        initial_state = {
            "job_description": jd_text,
            "resumes": resumes_data,
            "parsed_jd": None,
            "candidates": [],
            "ranked_shortlist": None,
            "messages": []
        }
        
        # Run the LangGraph workflow
        result = recruitment_pipeline.invoke(initial_state)

        # Prepare results for saving
        # For the history list, we'll use the top candidate and their score
        ranked_list = result.get("ranked_shortlist")
        top_resume_name = "Multi-Batch Analysis"
        top_match_percentage = 0
        
        if ranked_list and ranked_list.get("top_candidates"):
            top_candidate = ranked_list["top_candidates"][0]
            top_resume_name = f"{top_candidate['name']} & Others"
            top_match_percentage = top_candidate['score']

        # Save to Database
        user_id = "default_user" 
        save_analysis(user_id, jd_text, top_resume_name, top_match_percentage, result)

        # Mark session as success explicitly for AgentOps dashboard
        if AGENTOPS_API_KEY:
            agentops.end_session(end_state="Success")
            # Wait for background flush on Windows
            time.sleep(1)

        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        print(f"Error during analysis: {e}")
        traceback.print_exc()
        if AGENTOPS_API_KEY:
            agentops.end_session(end_state="Fail")
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files (if any in a separate folder inside frontend)
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# Frontend mounting removed as it is served by Nginx in local Docker setup,
# but handled above for unified cloud deployment.

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
