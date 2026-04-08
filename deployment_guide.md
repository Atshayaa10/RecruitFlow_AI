# Deployment Guide: RecruitFlow AI

This guide explains how to deploy the fully Dockerized RecruitFlow AI application to a publicly accessible URL.

## Prerequisites
- A cloud provider account (e.g., [Fly.io](https://fly.io/), [Railway](https://railway.app/), or any VPS with Docker installed).
- Your `AGENTOPS_API_KEY` and `GROQ_API_KEY`.

## Option 1: Quick Deployment with Railway (Recommended)

1.  **Fork/Upload**: Upload the project to a GitHub repository.
2.  **New Project**: In Railway.app, create a "New Project" and select "GitHub Repo".
3.  **Docker Compose**: Railway will automatically detect the `docker-compose.yml`.
4.  **Environment Variables**: Add the following variables to the **backend** service in Railway:
    - `GROQ_API_KEY`: Your Groq API key.
    - `AGENTOPS_API_KEY`: Your AgentOps API key.
    - `MODEL_NAME`: e.g., `llama-3.3-70b-versatile`.
5.  **Networking**: Railway will provide a public URL for the `frontend` service (port 80).

## Option 2: VPS with Docker Compose

If you have a Linux VPS (Ubuntu/Debian):

1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/your-repo/recruitment_automation.git
    cd recruitment_automation
    ```
2.  **Setup Environment**:
    Create `backend/.env` and add your keys.
3.  **Start the Stack**:
    ```bash
    docker compose up -d --build
    ```
4.  **Access**:
    The app will be available at `http://YOUR_SERVER_IP:8080`.

## Option 3: Unified Single-Container Deployment (Fly.io)

For the simplest public URL, you can merge the frontend and backend into a single container:

1.  **Update `main.py`**: Ensure `StaticFiles` mounting is active.
2.  **Deploy Backend**: Fly.io will serve the FastAPI app, which in turn serves the UI.

---

> [!TIP]
> **AgentOps Monitoring**: Once deployed, visit the [AgentOps Dashboard](https://app.agentops.ai/) to see real-time traces of your recruitment agents in production.
