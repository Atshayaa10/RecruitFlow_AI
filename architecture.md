# Project Architecture: RecruitFlow AI

This document provides a visual and technical overview of the multi-agent orchestration within RecruitFlow AI.

## 📊 System Architecture Diagram

```mermaid
graph TD
    classDef plain fill:#fff,stroke:#000,stroke-width:2px,color:#000;
    classDef agent fill:#f9f9f9,stroke:#000,stroke-width:2px,color:#000,stroke-dasharray: 5 5;
    
    subgraph UserInterface ["System Boundary: Frontend (Chat UI)"]
        A["Recruiter Uploads JD & Resumes"]:::plain
        B["Interactive Shortlist Results"]:::plain
    end

    subgraph Backend ["System Boundary: Unified Backend (FastAPI)"]
        C["API Endpoint (/analyze)"]:::plain
        D[(SQLite History DB/Persistence)]:::plain
        
        subgraph LangGraph ["Multi-Agent Orchestrator (LangGraph)"]
            E["JD Parser Agent"]:::agent
            F["Candidate Screener Agent\n(Rubric-based Evaluation)"]:::agent
            G["Ranking Agent\n(Comparative Shortlisting)"]:::agent
        end
    end

    subgraph ExternalServices ["External Ecosystem"]
        H["LLM Brain (Llama 3.3 via Groq)"]:::plain
        I["AgentOps (Real-time Observability)"]:::plain
    end

    %% Data Flow
    A --> C
    C --> E
    E --> F
    F --> G
    G --> B
    G --> D
    
    %% External Trace/Calls
    E -.-> H
    F -.-> H
    G -.-> H
    LangGraph -.-> I
```

## 🛠️ Tech Stack Overview
- **Orchestration**: LangGraph (Stateful Multi-Agent Workflows)
- **Backend API**: FastAPI (Python)
- **Frontend**: Vanilla Javascript + Tailwind CSS
- **Database**: SQLite (Local persistence)
- **Observability**: AgentOps (End-to-end tracing)
- **Deployment**: Render (Unified Docker Container)

---

> [!TIP]
> **AgentOps Integration**: Every node execution seen in the diagram above is tracked as a distinct event in your AgentOps explorer, allowing for full "Chain of Thought" auditing.
