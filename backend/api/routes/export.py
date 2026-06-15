# export.py
# Route handler for GET /api/export/{session_id}

import io
import json
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import Session as DBSession, Result as DBResult

router = APIRouter(prefix="/export", tags=["Export"])

@router.get("/{session_id}")
async def export_results(session_id: str, db: Session = Depends(get_db)):
    """
    Exports the ranking results of a session to a downloadable CSV file.
    Returns 404 if the session ID is not found.
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
    
    # 3. Build data list for pandas
    rows = []
    for r in db_results:
        resume = r.resume
        if not resume:
            continue
            
        try:
            skills = json.loads(resume.parsed_skills) if resume.parsed_skills else []
        except Exception:
            skills = []
            
        try:
            missing = json.loads(r.missing_keywords) if r.missing_keywords else []
        except Exception:
            missing = []
            
        rows.append({
            "rank": r.rank_position,
            "filename": resume.filename,
            "tfidf_score": r.tfidf_score,
            "sbert_score": r.sbert_score,
            "final_score": r.final_score,
            "missing_keywords": "|".join(missing),
            "skills_matched": "|".join(skills)
        })
        
    # 4. Build DataFrame and serialize to CSV stream
    df = pd.DataFrame(rows)
    if df.empty:
        df = pd.DataFrame(columns=[
            "rank", "filename", "tfidf_score", "sbert_score", 
            "final_score", "missing_keywords", "skills_matched"
        ])
        
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    # Stream response
    return StreamingResponse(
        io.BytesIO(csv_buffer.getvalue().encode("utf-8")),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=results_{session_id}.csv"}
    )
