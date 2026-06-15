# main.py
# FastAPI Application Entry Point for AI-Powered Resume Ranking System

import spacy
import spacy.cli
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import api_router
from backend.config import settings

app = FastAPI(
    title="AI-Powered Resume Ranking System",
    description="Backend API for ranking resumes based on TF-IDF and SBERT semantic similarities.",
    version="1.0.0",
    docs_url="/docs"
)

# CORS Middleware configuration (allow all origins for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    print("Starting up FastAPI application...")
    
    # Load spaCy NLP model into app state
    print("Loading spaCy NLP model ('en_core_web_sm')...")
    try:
        app.state.nlp = spacy.load("en_core_web_sm")
        print("spaCy model loaded successfully.")
    except Exception as e:
        print(f"Error loading spaCy model: {e}")
        # Try to download if not found
        try:
            print("Attempting to download 'en_core_web_sm'...")
            spacy.cli.download("en_core_web_sm")
            app.state.nlp = spacy.load("en_core_web_sm")
            print("spaCy model downloaded and loaded successfully.")
        except Exception as dl_err:
            print(f"Failed to download spaCy model: {dl_err}")

    # Load SBERT model into app state
    print(f"Loading SBERT model '{settings.SBERT_MODEL_NAME}'...")
    try:
        app.state.sbert = SentenceTransformer(settings.SBERT_MODEL_NAME)
        print("SBERT model loaded successfully.")
    except Exception as e:
        print(f"Error loading SBERT model: {e}")

@app.get("/")
async def root():
    return {
        "app": "AI-Powered Resume Ranking System API",
        "status": "active",
        "docs": "/docs"
    }
