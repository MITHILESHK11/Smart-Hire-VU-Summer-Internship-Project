# Dockerfile for Backend Service
FROM python:3.10-slim

WORKDIR /app

# Copy dependency definition
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download default spaCy model (English small web)
RUN python -m spacy download en_core_web_sm

# Copy backend codebase
COPY backend/ /app/backend/

EXPOSE 8000

# Placeholder CMD (entrypoint to be refined in Phase 6)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
