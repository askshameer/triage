# Multi-stage build for production deployment
FROM node:18-alpine AS frontend-builder

WORKDIR /frontend

# Copy frontend files
COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# Python backend stage
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application files
COPY triage_tool.py app.py ./
COPY error_mappings.xlsx* ./ 2>/dev/null || :

# Copy built frontend from previous stage
COPY --from=frontend-builder /frontend/dist ./static

# Create a simple Flask app to serve static files
RUN echo 'from flask import send_from_directory\n\
from app import app as original_app\n\
\n\
@original_app.route("/", defaults={"path": ""})\n\
@original_app.route("/<path:path>")\n\
def serve_frontend(path):\n\
    if path and path.startswith("api/"):\n\
        # Let API routes handle themselves\n\
        return original_app.view_functions[path.split("/")[1]]()\n\
    if path != "" and os.path.exists(os.path.join("static", path)):\n\
        return send_from_directory("static", path)\n\
    else:\n\
        return send_from_directory("static", "index.html")\n\
\n\
app = original_app' > serve.py

EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
