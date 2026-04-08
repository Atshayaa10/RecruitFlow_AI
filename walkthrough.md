# RecruitFlow AI Optimized for Render

I have successfully optimized the project for **One-Click Deployment on Render**. The entire application is now consolidated into a high-performance single-container architecture.

## 🚀 Deployment Status
- **GitHub Repository**: [https://github.com/Atshayaa10/RecruitFlow_AI.git](https://github.com/Atshayaa10/RecruitFlow_AI.git)
- **Deployment Strategy**: Unified Single Container (FastAPI serving UI).

## ✅ What I've Changed

### 1. Unified Single-Container Architecture
Render works best with individual web services. I have merged the frontend and backend into a single production Docker container.
- **[Dockerfile](file:///c:/Users/atsha/Downloads/recruitment_automation/Dockerfile)**: Rebuilt to bundle the UI and API together.
- **`backend/main.py`**: Updated to serve the premium interface at the root `/` URL while still handling all API requests.

### 2. Render Blueprint (`render.yaml`)
I've added a **Render Blueprint** file. This means when you connect your repo to Render, it will automatically:
- Detect the correct Docker environment.
- Provision a Web Service with the right names.
- Pre-set the required environment variables.

### 3. Detailed Deployment Guide
The **[deployment_guide.md](file:///c:/Users/atsha/Downloads/recruitment_automation/deployment_guide.md)** now contains a specific step-by-step section for Render.

---

## 📥 Your Next Steps on Render

1.  **Open [Render Dashboard](https://dashboard.render.com/)**.
2.  **New + > Web Service**.
3.  Connect the `Atshayaa10/RecruitFlow_AI` repository.
4.  Render will find the `render.yaml` and prompt you for:
    - `GROQ_API_KEY`
    - `AGENTOPS_API_KEY`
5.  Click **Deploy**, and your site will be live at a public `https://...` URL!

> [!IMPORTANT]
> **Health Check**: I've configured a `/health` endpoint so Render can monitor your service's uptime automatically.

> [!TIP]
> **Live Observability**: Once live, your AgentOps dashboard will begin receiving traces from your production URL immediately.
