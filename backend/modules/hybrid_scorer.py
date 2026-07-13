from typing import List, Dict, Any

def compute_hybrid_scores(
    tfidf_scores: List[float], 
    sbert_scores: List[float], 
    alpha: float = 0.4
) -> List[float]:
    """
    Combines TF-IDF and SBERT scores using a linear combination:
    Final Score = alpha * TF-IDF + (1 - alpha) * SBERT
    """
    if len(tfidf_scores) != len(sbert_scores):
        raise ValueError("TF-IDF and SBERT score lists must be of the same length.")
        
    hybrid_scores = []
    for tf_score, sb_score in zip(tfidf_scores, sbert_scores):
        combined = alpha * tf_score + (1.0 - alpha) * sb_score
        # Bound between 0.0 and 1.0
        combined = max(0.0, min(1.0, combined))
        hybrid_scores.append(float(combined))
        
    return hybrid_scores
