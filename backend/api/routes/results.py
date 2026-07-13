from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any
import logging

from backend.db.models import get_session, get_candidate_results, update_session_alpha, save_candidate_results
from backend.modules.hybrid_scorer import compute_hybrid_scores
from backend.modules.ranking import rank_candidates

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/results/{session_id}")
async def get_results(
    session_id: str,
    alpha: Optional[float] = Query(None, description="Adjust weights dynamically: Final Score = alpha * TF-IDF + (1-alpha) * SBERT")
):
    """
    Retrieves the ranked candidate results for a given session ID.
    If 'alpha' is provided, recalculates final scores and re-ranks candidates.
    """
    # 1. Fetch session
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
        
    jd_skills = session.get("jd_skills", [])
    
    # 2. Fetch candidate results
    candidates = get_candidate_results(session_id)
    if not candidates:
        raise HTTPException(status_code=404, detail="No candidates found for this session.")
        
    # 3. If alpha weight is dynamically adjusted, re-score and re-rank
    if alpha is not None:
        if not (0.0 <= alpha <= 1.0):
            raise HTTPException(status_code=400, detail="Alpha weight must be between 0.0 and 1.0.")
            
        logger.info(f"Recalculating session {session_id} with new alpha weight: {alpha}")
        
        # Update session alpha in database
        update_session_alpha(session_id, alpha)
        
        # Prepare lists for hybrid scoring (retrieve raw 0-1 values from saved percentage scores)
        tfidf_scores = [c["tfidf_score"] / 100.0 for c in candidates]
        sbert_scores = [c["sbert_score"] / 100.0 for c in candidates]
        
        # Recalculate hybrid scores
        new_hybrid_scores = compute_hybrid_scores(tfidf_scores, sbert_scores, alpha)
        
        # Enrich candidates with new final score
        candidates_raw_data = []
        for idx, cand in enumerate(candidates):
            # Maintain existing attributes, update final_score
            cand_raw = {
                **cand,
                "final_score": round(new_hybrid_scores[idx] * 100, 1)
            }
            candidates_raw_data.append(cand_raw)
            
        # Re-rank candidates using new scores
        ranked_candidates = rank_candidates(candidates_raw_data, jd_skills)
        
        # Save updated ranks to the database
        try:
            save_candidate_results(session_id, ranked_candidates)
        except Exception as e:
            logger.error(f"Failed to save re-ranked candidates to database: {e}")
            
        # Set candidates to the newly ranked set
        candidates = ranked_candidates
        session["alpha"] = alpha
        
    return {
        "session_id": session_id,
        "alpha": session["alpha"],
        "required_skills": jd_skills,
        "candidates": candidates
    }
