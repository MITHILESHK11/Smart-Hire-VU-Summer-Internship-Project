import logging
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

logger = logging.getLogger(__name__)

# Global model holder for lazy-loading
_sbert_model = None

def get_sbert_model():
    """Initializes and returns the SentenceTransformer model (singleton)."""
    global _sbert_model
    if _sbert_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            logger.info("Loading Sentence-BERT model (all-MiniLM-L6-v2)...")
            _sbert_model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("Sentence-BERT model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load SBERT model: {e}")
            raise RuntimeError(f"Could not load Sentence-BERT model: {e}")
    return _sbert_model

def compute_sbert_similarity(jd_text: str, resume_texts: List[str]) -> List[float]:
    """
    Computes semantic similarity scores using Sentence-BERT embeddings.
    Uses batch encoding for performance optimization.
    """
    if not resume_texts:
        return []
        
    model = get_sbert_model()
    
    try:
        # Encode job description (single query)
        jd_embedding = model.encode(jd_text, convert_to_numpy=True).reshape(1, -1)
        
        # Batch encode resumes (returns a 2D matrix of shape [num_resumes, embedding_dim])
        resume_embeddings = model.encode(resume_texts, batch_size=16, show_progress_bar=False, convert_to_numpy=True)
        
        # Compute cosine similarity
        similarities = cosine_similarity(resume_embeddings, jd_embedding).flatten()
        
        return [float(score) for score in similarities]
    except Exception as e:
        logger.error(f"Error in SBERT similarity computation: {e}")
        # Fallback to 0.0 scores
        return [0.0] * len(resume_texts)
