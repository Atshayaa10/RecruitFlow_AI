# RecruitFlow AI - Multi-Agent Recruitment Automation

RecruitFlow AI is a premium, ChatGPT-inspired multi-agent application designed to automate candidate screening and shortlisting. Built on **LangGraph** and instrumented with **AgentOps**, it processes job descriptions and multiple resumes to deliver ranked shortlists with detailed interview strategies.

## 🚀 Live Demo
**URL**: [Coming Soon / Your Deployment URL]

## ✨ Features
- **Multi-Agent Orchestration**: Uses LangGraph to coordinate JD Parsing, Candidate Screening, and Batch Ranking.
- **Precision Scoring**: Implements a 100-point rubric (Skills, Experience, Education) for differentiated candidate evaluations.
- **ChatGPT Aesthetic**: A glassmorphic, dark-mode interface with interactive, collapsible candidate deep-dives.
- **Observability**: Fully instrumented with AgentOps for real-time agent tracing and monitoring.
- **Dockerized Architecture**: Nginx-based reverse proxy serving a frontend + FastAPI backend.

## 🛠️ Architecture
- **Orchestrator**: LangGraph (StateGraph)
- **Agents**:
  - `JD Parser`: Extracts structured requirements.
  - `Candidate Screener`: Rubric-based evaluation of individual resumes.
  - `Ranking Agent`: Comparative ranking of the candidate pool.
- **Backend**: FastAPI, SQLite, Pydantic, PyPDF.
- **Frontend**: Vanilla JS, Tailwind CSS, Axios.
- **Infrastructure**: Docker, Docker Compose, Nginx.

## 📦 Setup & Installation

### 1. Prerequisites
- Docker & Docker Compose
- [Groq API Key](https://console.groq.com/)
- [AgentOps API Key](https://app.agentops.ai/)

### 2. Environment Configuration
Create a `.env` file in the `backend/` directory:
```env
GROQ_API_KEY=your_groq_key
AGENTOPS_API_KEY=your_agentops_key
MODEL_NAME=llama-3.3-70b-versatile
```

### 3. Run with Docker
```bash
docker-compose up --build
```
Access the application at **`http://localhost:8080`**.

## 📄 License
MIT License
