# config.py
# Application Configurations for AI-Powered Resume Ranking System

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Settings:
    # Formula Weight (default alpha = 0.3)
    ALPHA_WEIGHT: float = float(os.getenv("ALPHA_WEIGHT", "0.3"))
    
    # SBERT Semantic Embedding Model
    SBERT_MODEL_NAME: str = os.getenv("SBERT_MODEL_NAME", "all-MiniLM-L6-v2")
    
    # Database Settings
    DB_PATH: str = os.getenv("DB_PATH", str(BASE_DIR / "db" / "resume_ranking.db"))
    
    # Ingestion Settings
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", str(BASE_DIR.parent / "test_data" / "resumes"))
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "5"))

settings = Settings()
