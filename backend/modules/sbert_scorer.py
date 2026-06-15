# sbert_scorer.py
# Module 4B: Sentence-BERT Semantic Scoring Engine

from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from backend.config import settings

_sbert_model = None

def load_sbert_model(model_name: str = settings.SBERT_MODEL_NAME) -> SentenceTransformer:
    """Loads and caches the Sentence-BERT model (Singleton pattern)."""
    global _sbert_model
    if _sbert_model is None:
        _sbert_model = SentenceTransformer(model_name)
    return _sbert_model

def encode_text(model, text: str) -> np.ndarray:
    """Encodes a single string text into a normalized SBERT dense vector."""
    if not text or not text.strip():
        # Default zero-filled vector matching MiniLM 384 dimensions
        return np.zeros(384)
    # Enable normalize_embeddings to compute cosine similarity directly via dot product or cosine_similarity
    return model.encode(text, normalize_embeddings=True)

def batch_encode(model, texts: list[str], batch_size=16) -> np.ndarray:
    """Encodes a list of string texts in batches with normalized embeddings."""
    if not texts:
        return np.empty((0, 384))
    cleaned_texts = [t if (t and t.strip()) else "" for t in texts]
    return model.encode(cleaned_texts, batch_size=batch_size, normalize_embeddings=True)

def compute_sbert_similarity(jd_text: str, resume_texts: list[str]) -> list[float]:
    """Computes semantic similarity scores between a job description and a list of resumes using SBERT."""
    if not resume_texts:
        return []
        
    model = load_sbert_model()
    
    # Encode JD (1, D)
    jd_embedding = encode_text(model, jd_text).reshape(1, -1)
    
    scores = []
    for text in resume_texts:
        if not text or not text.strip():
            scores.append(0.0)
            continue
            
        resume_embedding = encode_text(model, text).reshape(1, -1)
        # Cosine similarity calculation
        similarity = cosine_similarity(jd_embedding, resume_embedding)[0][0]
        # Map values to positive range 0.0 - 1.0 (cosine sim of normalised vectors ranges -1 to 1)
        # Cosine similarity on SBERT embeddings is typically >= 0, but clip it just in case
        similarity = float(np.clip(similarity, 0.0, 1.0))
        scores.append(similarity)
        
    return scores
