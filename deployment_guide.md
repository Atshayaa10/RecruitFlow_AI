# Deployment Guide: RecruitFlow AI

This guide explains how to deploy the fully Dockerized RecruitFlow AI application to a publicly accessible URL.

## Prerequisites
- A cloud provider account (e.g., [Fly.io](https://fly.io/), [Railway](https://railway.app/), or any VPS with Docker installed).
- Your `AGENTOPS_API_KEY` and `GROQ_API_KEY`.

## Option 1: One-Click Deploy to Render (Recommended)

Render is the simplest way to get RecruitFlow AI live. We have optimized the project into a **Unified Single Container** that hosts both the frontend and backend.

### Steps:
1.  **Push to GitHub**: Ensure your latest changes (including the new root `Dockerfile` and `render.yaml`) are pushed to your GitHub repo.
2.  **Create New Web Service**:
    - Log in to [Render](https://dashboard.render.com/).
    - Click **New +** > **Web Service**.
    - Connect your GitHub repository.
3.  **Configure**:
    - **Name**: `recruitflow-ai`
    - **Environment**: `Docker` (Render will automatically detect the root `Dockerfile`).
4.  **Environment Variables**: Add the following in the "Environment" tab:
    - `GROQ_API_KEY`: Your Groq API key.
    - `AGENTOPS_API_KEY`: Your AgentOps API key.
    - `MODEL_NAME`: `llama-3.3-70b-versatile`
5.  **Deploy**: Click **Create Web Service**. Render will build the image and provide a public `https://...` URL.

---

## Option 3: VPS with Docker Compose (Local/Private)

---

> [!TIP]
> **AgentOps Monitoring**: Once deployed, visit the [AgentOps Dashboard](https://app.agentops.ai/) to see real-time traces of your recruitment agents in production.
