import csv
import io
import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from backend.db.models import get_session, get_candidate_results

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/export/{session_id}")
async def export_results_csv(session_id: str):
    """
    Exports the ranked candidate results for a given session ID as a CSV download.
    """
    # 1. Fetch session and candidate results
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
        
    candidates = get_candidate_results(session_id)
    if not candidates:
        raise HTTPException(status_code=404, detail="No candidate results found for this session.")
        
    # 2. Build CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header columns
    writer.writerow([
        "Rank", 
        "Candidate Filename", 
        "Lexical Score (TF-IDF %)", 
        "Semantic Score (SBERT %)", 
        "Final Match %", 
        "Years of Experience",
        "Matched Skills", 
        "Missing Skills", 
        "Education", 
        "Job Titles"
    ])
    
    # Write candidate rows
    for cand in candidates:
        writer.writerow([
            cand["rank"],
            cand["filename"],
            cand["tfidf_score"],
            cand["sbert_score"],
            cand["final_score"],
            cand["years_of_experience"],
            ", ".join(cand.get("matched_skills", [])),
            ", ".join(cand.get("missing_skills", [])),
            ", ".join(cand.get("education", [])),
            ", ".join(cand.get("job_titles", []))
        ])
        
    # Rewind buffer
    output.seek(0)
    
    filename = f"ranked_candidates_{session_id}.csv"
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )
