import os
import time
import logging
import traceback
from datetime import datetime
from typing import List, Optional
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# --- Minimal Configuration ---
# Absolute path resolution
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = Path("/app/frontend")

from database import init_db, save_analysis, get_history, get_analysis_detail
from utils import extract_text_from_pdf

# Initialize DB on startup
init_db()

app = FastAPI(title="RecruitFlow AI API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return "RecruitFlow AI API is running. Frontend not found in /app/frontend"

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/history")
async def fetch_history(user_id: str = "default_user"):
    return {"status": "success", "data": get_history(user_id)}

@app.get("/history/{analysis_id}")
async def fetch_detail(analysis_id: int):
    detail = get_analysis_detail(analysis_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return {"status": "success", "data": detail}

@app.post("/analyze")
async def analyze_recruitment(
    jd_text: str = Form(...),
    resume_files: List[UploadFile] = File(...)
):
    print(f"[{datetime.now()}] Request received: {len(resume_files)} files")
    
    # LAZY LOADING: Load agents only when needed to save memory during boot
    try:
        from agents import recruitment_pipeline
    except Exception as e:
        print(f"ERROR: Could not load agents pipeline: {e}")
        raise HTTPException(status_code=500, detail="AI Pipeline failed to load")

    try:
        resumes_data = []
        for resume_file in resume_files:
            resume_bytes = await resume_file.read()
            resume_text = extract_text_from_pdf(resume_bytes)
            if resume_text:
                resumes_data.append({"filename": resume_file.filename, "text": resume_text})

        if not resumes_data:
            raise HTTPException(status_code=400, detail="Could not extract text from any PDF")

        initial_state = {
            "job_description": jd_text,
            "resumes": resumes_data,
            "parsed_jd": None,
            "candidates": [],
            "ranked_shortlist": None,
            "messages": []
        }
        
        result = recruitment_pipeline.invoke(initial_state)

        ranked_list = result.get("ranked_shortlist")
        top_resume_name = "Multi-Batch Analysis"
        top_match_percentage = 0
        
        if ranked_list and ranked_list.get("top_candidates"):
            top_candidate = ranked_list["top_candidates"][0]
            top_resume_name = f"{top_candidate['name']} & Others"
            top_match_percentage = top_candidate['score']

        save_analysis("default_user", jd_text, top_resume_name, top_match_percentage, result)
        return {"status": "success", "data": result}
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
