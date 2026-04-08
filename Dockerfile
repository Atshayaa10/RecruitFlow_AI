# Production Dockerfile for Unified Deployment (Render/Fly.io)
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for PDF processing
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and frontend
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Set working directory to backend to run the app
WORKDIR /app/backend

# Create a placeholder for the database
RUN touch recruitment.db

EXPOSE 8000

# Start FastAPI
CMD ["python", "main.py"]
