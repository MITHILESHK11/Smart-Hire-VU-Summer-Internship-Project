# hybrid_scorer.py
# Module 4C: Hybrid Scoring Engine

from backend.modules.tfidf_scorer import compute_tfidf_similarity
from backend.modules.sbert_scorer import compute_sbert_similarity
from backend.config import settings

def compute_hybrid_scores(
    jd_text: str,
    resume_texts: list[str],
    alpha: float = settings.ALPHA_WEIGHT
) -> list[dict]:
    """
    Computes a hybrid matching score for a batch of resumes vs. a job description.
    
    Formula:
      Final Score = alpha * TF-IDF + (1 - alpha) * SBERT
      
    Returns a list of dicts:
      {tfidf_score, sbert_score, final_score, resume_index}
    """
    if not resume_texts:
        return []
        
    # 1. Compute lexical matching scores (TF-IDF)
    tfidf_scores = compute_tfidf_similarity(jd_text, resume_texts)
    
    # 2. Compute semantic matching scores (SBERT)
    sbert_scores = compute_sbert_similarity(jd_text, resume_texts)
    
    # 3. Combine scores using configured/passed alpha weight
    hybrid_results = []
    for idx, (tf_score, sb_score) in enumerate(zip(tfidf_scores, sbert_scores)):
        final_score = alpha * tf_score + (1.0 - alpha) * sb_score
        
        # Keep results clean with rounding to 4 decimal places
        hybrid_results.append({
            "tfidf_score": round(tf_score, 4),
            "sbert_score": round(sb_score, 4),
            "final_score": round(final_score, 4),
            "resume_index": idx
        })
        
    return hybrid_results
