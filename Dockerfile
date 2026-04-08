# Production Dockerfile for Unified Deployment (Render/Fly.io)
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for PDF processing
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy backend and frontend to absolute paths
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/

# Set working directory to backend to run the app
WORKDIR /app/backend

# Create a placeholder for the database
RUN touch /app/backend/recruitment.db

# Ensure logs are visible and real-time
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8

# Port hint for Render
EXPOSE 10000

# Start Gunicorn with Uvicorn workers for production stability
# Use shell form to allow environment variable expansion (for Render's dynamic PORT)
CMD gunicorn -w 1 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT:-10000} --timeout 120
