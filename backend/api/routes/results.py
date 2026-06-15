# results.py
# Route handler for GET /api/results/{session_id}

import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import Session as DBSession, Result as DBResult

router = APIRouter(prefix="/results", tags=["Results"])

@router.get("/{session_id}")
async def get_results(session_id: str, db: Session = Depends(get_db)):
    """
    Retrieves the job description and ranked candidates for a given session ID.
    Returns 404 if the session ID is invalid or not found.
    """
    # 1. Fetch Session
    db_session = db.query(DBSession).filter(DBSession.session_id == session_id).first()
    if not db_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID '{session_id}' not found."
        )
        
    # 2. Fetch associated results ordered by rank_position
    db_results = db.query(DBResult).filter(
        DBResult.session_id == session_id
    ).order_by(DBResult.rank_position.asc()).all()
    
    # 3. Assemble ranked_candidates payload
    ranked_candidates = []
    for r in db_results:
        resume = r.resume
        if not resume:
            continue
            
        try:
            skills = json.loads(resume.parsed_skills) if resume.parsed_skills else []
        except Exception:
            skills = []
            
        try:
            edu = json.loads(resume.parsed_education) if resume.parsed_education else []
        except Exception:
            edu = []
            
        try:
            exp_data = json.loads(resume.parsed_experience) if resume.parsed_experience else {}
            exp_years = exp_data.get("years")
        except Exception:
            exp_years = None
            
        try:
            missing = json.loads(r.missing_keywords) if r.missing_keywords else []
        except Exception:
            missing = []
            
        ranked_candidates.append({
            "rank": r.rank_position,
            "filename": resume.filename,
            "tfidf_score": r.tfidf_score,
            "sbert_score": r.sbert_score,
            "final_score": r.final_score,
            "missing_keywords": missing,
            "skills_matched": skills,
            "education": edu,
            "experience_years": exp_years
        })
        
    # Formatting datetime created_at field
    created_at_iso = db_session.created_at.isoformat() if hasattr(db_session.created_at, "isoformat") else str(db_session.created_at)
    
    return {
        "session_id": db_session.session_id,
        "created_at": created_at_iso,
        "jd_text": db_session.jd_text,
        "ranked_candidates": ranked_candidates
    }
