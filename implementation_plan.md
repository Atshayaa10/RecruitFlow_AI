# Fix Render Error 521 (Connection Refused)

The user is experiencing a "Web server is down Error code 521" on their Render deployment. This typically means the Render proxy cannot connect to the backend container. Most common causes are the app crashing on startup, listening on the wrong port, or failing health checks.

## User Review Required

> [!IMPORTANT]
> Since I cannot access the live Render logs, these changes are designed to improve robustness and visibility. Please check your **Render Dashboard Logs** after these changes are pushed.

## Proposed Changes

### [Backend]

Improve `main.py` to be more resilient and provide better diagnostic logs on Render.

#### [MODIFY] [main.py](file:///c:/Users/atsha/Downloads/recruitment_automation/backend/main.py)
- Explicitly log the port the server is listening on.
- Ensure `agentops` initialization is protected and doesn't block.
- Add more robust handling for the frontend path.

#### [MODIFY] [Dockerfile](file:///c:/Users/atsha/Downloads/recruitment_automation/Dockerfile)
- Add `EXPOSE 8000` as a hint (though `PORT` is dynamic).
- Ensure the working directory and environment variables are optimal for production.

#### [MODIFY] [render.yaml](file:///c:/Users/atsha/Downloads/recruitment_automation/render.yaml)
- Ensure the health check is correctly configured.

## Open Questions
- Have you verified that `GROQ_API_KEY` is definitely set in the Render Dashboard? If it's missing, the app might crash before it can serve the health check.

## Verification Plan

### Automated Tests
- I will run the container locally using a dummy `PORT` env var to verify it listens correctly and responds to `/health`.

### Manual Verification
- Ask the user to push the changes and check the Render logs if it still fails.
