import os
import sys

# Ensure backend is in search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.modules.ingestion import extract_text
from backend.modules.preprocessing import preprocess_text
from backend.modules.ner import run_ner
from backend.modules.tfidf_scorer import compute_tfidf_similarity
from backend.modules.sbert_scorer import compute_sbert_similarity
from backend.modules.hybrid_scorer import compute_hybrid_scores
from backend.modules.ranking import rank_candidates
from backend.db.models import init_db, save_session, save_candidate_results, get_candidate_results

def test_pipeline():
    print("=== Initializing Test DB ===")
    init_db()
    
    print("\n=== Loading Job Description ===")
    jd_path = "test_data/jd.txt"
    with open(jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()
    print(f"Loaded Job Description from {jd_path} ({len(jd_text)} chars)")
    
    # Run NER on JD
    jd_ner = run_ner(jd_text)
    print(f"Job Description extracted skills: {jd_ner['skills']}")
    
    print("\n=== Loading Resumes ===")
    resume_files = [
        "test_data/resumes/john_doe_perfect.pdf",
        "test_data/resumes/jane_smith_semantic.docx",
        "test_data/resumes/bob_johnson_weak.pdf"
    ]
    
    parsed_resumes = []
    for filepath in resume_files:
        filename = os.path.basename(filepath)
        with open(filepath, "rb") as f:
            content = f.read()
        text = extract_text(content, filename)
        parsed_resumes.append({
            "filename": filename,
            "raw_text": text
        })
        print(f"Extracted {len(text)} chars from {filename}")
        
    print("\n=== Preprocessing ===")
    jd_processed = preprocess_text(jd_text)
    resume_processed_list = [preprocess_text(r["raw_text"]) for r in parsed_resumes]
    
    print("\n=== TF-IDF Scoring ===")
    tfidf_scores = compute_tfidf_similarity(jd_processed, resume_processed_list)
    for res, score in zip(parsed_resumes, tfidf_scores):
        print(f"  {res['filename']}: {score:.4f}")
        
    print("\n=== SBERT Scoring ===")
    sbert_scores = compute_sbert_similarity(jd_text, [r["raw_text"] for r in parsed_resumes])
    for res, score in zip(parsed_resumes, sbert_scores):
        print(f"  {res['filename']}: {score:.4f}")
        
    print("\n=== Hybrid Scoring (alpha=0.4) ===")
    alpha = 0.4
    hybrid_scores = compute_hybrid_scores(tfidf_scores, sbert_scores, alpha)
    for res, score in zip(parsed_resumes, hybrid_scores):
        print(f"  {res['filename']}: {score:.4f}")
        
    # Enriched candidates
    candidates_raw_data = []
    for idx, res in enumerate(parsed_resumes):
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
        
    print("\n=== Ranking ===")
    ranked_candidates = rank_candidates(candidates_raw_data, jd_ner["skills"])
    for c in ranked_candidates:
        print(f"Rank {c['rank']}: {c['filename']}")
        print(f"  Final Score: {c['final_score']}% (TF-IDF: {c['tfidf_score']}%, SBERT: {c['sbert_score']}%)")
        print(f"  Experience: {c['years_of_experience']} yrs")
        print(f"  Matched Skills: {c['matched_skills']}")
        print(f"  Missing Skills: {c['missing_skills']}")
        print("-" * 40)
        
    print("\n=== Database Storage Verification ===")
    session_id = "test-session-123"
    save_session(session_id, jd_text, jd_ner["skills"], alpha)
    save_candidate_results(session_id, ranked_candidates)
    
    db_results = get_candidate_results(session_id)
    print(f"Successfully retrieved {len(db_results)} candidates from DB for session '{session_id}'")
    assert len(db_results) == 3, "Database save/load integrity failed"
    print("Database verify passed!")
    print("\n=== End-to-End Pipeline Verification Success ===")

if __name__ == "__main__":
    test_pipeline()
