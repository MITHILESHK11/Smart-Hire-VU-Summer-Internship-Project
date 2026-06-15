# rank.py
# Route handler for POST /api/rank

import time
import uuid
import json
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request, status
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import Session as DBSession, Resume as DBResume, Result as DBResult
from backend.config import settings
from backend.modules.ingestion import process_uploads
from backend.modules.ner import extract_entities
from backend.modules.hybrid_scorer import compute_hybrid_scores
from backend.modules.ranking import build_ranking_output

router = APIRouter(prefix="/rank", tags=["Rank"])

@router.post("")
async def rank_resumes(
    request: Request,
    jd_text: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Accepts job description text and batch resumes, processes them, 
    calculates scores, and persists results to database.
    """
    # 1. Input validation
    if not jd_text or not jd_text.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Job description text is required."
        )
        
    jd_len = len(jd_text.strip())
    if jd_len < 50 or jd_len > 10000:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Job description length must be between 50 and 10000 characters. Provided: {jd_len}"
        )
        
    # Read files list from multipart form fields
    form = await request.form()
    files = form.getlist("files[]") or form.getlist("files")
    
    if not files:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one resume file must be uploaded under key 'files[]' or 'files'."
        )
        
    if len(files) > 50:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Maximum limit is 50 resumes per request. Provided: {len(files)}"
        )
        
    # 2. Initialize database session record
    session_id = str(uuid.uuid4())
    db_session = DBSession(
        session_id=session_id,
        jd_text=jd_text,
        status="PROCESSING"
    )
    db.add(db_session)
    db.commit()
    
    start_time = time.time()
    
    try:
        # 3. Process uploads
        upload_dir = os.path.join(settings.UPLOAD_DIR, session_id)
        uploads = process_uploads(files, upload_dir)
        
        success_uploads = [u for u in uploads if u["status"] == "success"]
        
        # Graceful handling if no valid/supported files processed
        if not success_uploads:
            db_session.status = "COMPLETED"
            db.commit()
            
            processing_time_ms = int((time.time() - start_time) * 1000)
            return {
                "session_id": session_id,
                "ranked_candidates": [],
                "processing_time_ms": processing_time_ms
            }
            
        # 4. Process files and extract entities
        db_resumes = []
        resume_texts = []
        ner_results = []
        filenames = []
        
        for u in success_uploads:
            filename = u["filename"]
            raw_text = u["raw_text"]
            
            # Named Entity Recognition
            ner_info = extract_entities(raw_text)
            
            resume_id = str(uuid.uuid4())
            db_resume = DBResume(
                resume_id=resume_id,
                session_id=session_id,
                filename=filename,
                raw_text=raw_text,
                parsed_skills=json.dumps(ner_info["skills"]),
                parsed_education=json.dumps(ner_info["education"]),
                parsed_experience=json.dumps({"years": ner_info["years_experience"]})
            )
            db.add(db_resume)
            db_resumes.append(db_resume)
            
            resume_texts.append(raw_text)
            ner_results.append(ner_info)
            filenames.append(filename)
            
        db.commit()
        
        # 5. Hybrid Scoring
        scored_resumes = compute_hybrid_scores(jd_text, resume_texts, alpha=settings.ALPHA_WEIGHT)
        
        # 6. Rank Candidates and compute keyword gaps
        ranked_candidates = build_ranking_output(
            session_id=session_id,
            filenames=filenames,
            scored_resumes=scored_resumes,
            resume_texts=resume_texts,
            jd_text=jd_text,
            ner_results=ner_results
        )
        
        # 7. Persist Results to database
        resume_by_filename = {r.filename: r for r in db_resumes}
        for item in ranked_candidates:
            filename = item["filename"]
            db_resume = resume_by_filename[filename]
            
            result_id = str(uuid.uuid4())
            db_result = DBResult(
                result_id=result_id,
                session_id=session_id,
                resume_id=db_resume.resume_id,
                tfidf_score=item["tfidf_score"],
                sbert_score=item["sbert_score"],
                final_score=item["final_score"],
                missing_keywords=json.dumps(item["missing_keywords"]),
                rank_position=item["rank"]
            )
            db.add(db_result)
            
        # Complete session update
        db_session.status = "COMPLETED"
        db.commit()
        
        processing_time_ms = int((time.time() - start_time) * 1000)
        return {
            "session_id": session_id,
            "ranked_candidates": ranked_candidates,
            "processing_time_ms": processing_time_ms
        }
        
    except Exception as e:
        # Mark session as failed
        db_session.status = "FAILED"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pipeline processing failed: {str(e)}"
        )
