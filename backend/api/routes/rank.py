import uuid
import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List, Optional
import json

from backend.modules.ingestion import extract_text
from backend.modules.preprocessing import preprocess_text
from backend.modules.ner import run_ner
from backend.modules.tfidf_scorer import compute_tfidf_similarity
from backend.modules.sbert_scorer import compute_sbert_similarity
from backend.modules.hybrid_scorer import compute_hybrid_scores
from backend.modules.ranking import rank_candidates
from backend.db.models import save_session, save_candidate_results
from backend.api.middleware.validation import validate_uploaded_files, validate_job_description

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/rank")
async def rank_resumes(
    resumes: List[UploadFile] = File(...),
    job_description: str = Form(...),
    alpha: float = Form(0.4)
):
    """
    Accepts resumes (PDF/DOCX) and a job description (text),
    runs the NLP pipeline, scores and ranks them, stores the session,
    and returns the ranked candidates.
    """
    # 0. Validate inputs
    validate_uploaded_files(resumes)
    validate_job_description(job_description)
    
    session_id = str(uuid.uuid4())
    logger.info(f"Starting resume ranking session {session_id} with {len(resumes)} files.")
    
    # 1. Parse and extract text from resumes
    parsed_resumes = []
    failed_files = []
    
    for file in resumes:
        try:
            content = await file.read()
            text = extract_text(content, file.filename)
            if not text.strip():
                failed_files.append({"filename": file.filename, "error": "Empty file content"})
                continue
            parsed_resumes.append({
                "filename": file.filename,
                "raw_text": text
            })
        except Exception as e:
            logger.error(f"Failed to ingest resume '{file.filename}': {e}")
            failed_files.append({"filename": file.filename, "error": str(e)})
            
    if not parsed_resumes:
        raise HTTPException(
            status_code=422, 
            detail=f"Failed to parse any of the uploaded resumes. Failures: {json.dumps(failed_files)}"
        )
        
    # 2. Extract skills from Job Description using NER
    jd_ner = run_ner(job_description)
    jd_skills = jd_ner["skills"]
    
    # 3. Preprocess Job Description and Resume texts
    jd_processed = preprocess_text(job_description)
    resume_processed_list = []
    for res in parsed_resumes:
        resume_processed_list.append(preprocess_text(res["raw_text"]))
        
    # 4. Compute TF-IDF (lexical) Scores
    try:
        tfidf_scores = compute_tfidf_similarity(jd_processed, resume_processed_list)
    except Exception as e:
        logger.error(f"TF-IDF scoring failed: {e}")
        tfidf_scores = [0.0] * len(parsed_resumes)
        
    # 5. Compute SBERT (semantic) Scores
    try:
        sbert_scores = compute_sbert_similarity(job_description, [res["raw_text"] for res in parsed_resumes])
    except Exception as e:
        logger.error(f"SBERT scoring failed: {e}")
        sbert_scores = [0.0] * len(parsed_resumes)
        
    # 6. Compute Hybrid Scores
    hybrid_scores = compute_hybrid_scores(tfidf_scores, sbert_scores, alpha)
    
    # 7. Extract Profile Structures (NER) for resumes
    candidates_raw_data = []
    for idx, res in enumerate(parsed_resumes):
        # Extract features (skills, education, titles, experience) from original text
        ner_results = run_ner(res["raw_text"])
        
        candidates_raw_data.append({
            "filename": res["filename"],
            "raw_text": res["raw_text"],
            "tfidf_score": round(tfidf_scores[idx] * 100, 1),
            "sbert_score": round(sbert_scores[idx] * 100, 1),
            "final_score": round(hybrid_scores[idx] * 100, 1),
            "skills": ner_results["skills"],
            "education": ner_results["education"],
            "job_titles": ner_results["job_titles"],
            "years_of_experience": round(ner_results["years_of_experience"], 1)
        })
        
    # 8. Rank candidates & compute keyword gaps
    ranked_candidates = rank_candidates(candidates_raw_data, jd_skills)
    
    # 9. Persistent Storage in SQLite
    try:
        save_session(session_id, job_description, jd_skills, alpha)
        save_candidate_results(session_id, ranked_candidates)
    except Exception as e:
        logger.error(f"Failed to persist session in DB: {e}")
        # Continue and return response even if database storage fails
        
    return {
        "session_id": session_id,
        "alpha": alpha,
        "required_skills": jd_skills,
        "candidates": ranked_candidates,
        "failed_files": failed_files
    }
