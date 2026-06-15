# main.py
# FastAPI Application Entry Point for AI-Powered Resume Ranking System

import spacy
import spacy.cli
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.api.routes import api_router
from backend.config import settings
from backend.db.database import init_db
from backend.api.middleware.validation import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)

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

# Register Exception Handlers for uniform error JSON formatting
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include API Router
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    print("Starting up FastAPI application...")
    
    # Initialize SQLite Database tables
    print("Initializing Database...")
    try:
        init_db()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
        
    # Load spaCy NLP model into app state
    print("Loading spaCy NLP model ('en_core_web_sm')...")
    try:
        app.state.nlp = spacy.load("en_core_web_sm")
        print("spaCy model loaded successfully.")
    except Exception as e:
        print(f"Error loading spaCy model: {e}")
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

