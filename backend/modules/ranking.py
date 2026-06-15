# ranking.py
# Module 5: Ranking and Keyword Gap Analysis

import re
from backend.modules.tfidf_scorer import get_top_tfidf_keywords

def rank_candidates(scored_resumes: list[dict]) -> list[dict]:
    """Sorts candidates by final_score descending and adds a rank index (1..N)."""
    sorted_resumes = sorted(scored_resumes, key=lambda x: x["final_score"], reverse=True)
    for rank_idx, resume in enumerate(sorted_resumes, start=1):
        resume["rank"] = rank_idx
    return sorted_resumes

def compute_keyword_gap(jd_keywords: list[str], resume_text: str) -> list[str]:
    """Identifies keywords from the JD that are missing in the resume text (case-insensitive)."""
    if not jd_keywords:
        return []
    if not resume_text or not resume_text.strip():
        return jd_keywords
        
    resume_lower = resume_text.lower()
    missing_keywords = []
    
    for kw in jd_keywords:
        kw_lower = kw.lower()
        # Word boundary handling for symbols vs alpha keywords
        if kw_lower.endswith("+") or kw_lower.endswith(".js"):
            pattern = rf"\b{re.escape(kw_lower)}(?:\b|\s|$)"
        else:
            pattern = rf"\b{re.escape(kw_lower)}\b"
            
        if not re.search(pattern, resume_lower):
            missing_keywords.append(kw)
            
    return missing_keywords

def build_ranking_output(
    session_id: str,
    filenames: list[str],
    scored_resumes: list[dict],
    resume_texts: list[str],
    jd_text: str,
    ner_results: list[dict]
) -> list[dict]:
    """
    Combines scored resumes, raw texts, and NER results into a single formatted list,
    performs keyword gap analysis, sorts them, and assigns final ranks.
    
    Returns a list of dicts:
      {rank, filename, tfidf_score, sbert_score, final_score, missing_keywords, skills_matched, education, experience_years}
    """
    # 1. Extract top keywords from JD for gap calculations (using top 15 terms)
    jd_keywords = get_top_tfidf_keywords(jd_text, top_n=15)
    
    # Map scored_resumes by resume_index for direct index lookups
    scored_map = {item["resume_index"]: item for item in scored_resumes}
    
    raw_outputs = []
    for idx, filename in enumerate(filenames):
        score_info = scored_map.get(idx, {"tfidf_score": 0.0, "sbert_score": 0.0, "final_score": 0.0})
        resume_text = resume_texts[idx] if idx < len(resume_texts) else ""
        ner_info = ner_results[idx] if idx < len(ner_results) else {"skills": [], "education": [], "years_experience": None}
        
        # 2. Run keyword gap comparison
        missing = compute_keyword_gap(jd_keywords, resume_text)
        
        raw_outputs.append({
            "resume_index": idx,
            "filename": filename,
            "tfidf_score": score_info["tfidf_score"],
            "sbert_score": score_info["sbert_score"],
            "final_score": score_info["final_score"],
            "missing_keywords": missing,
            "skills_matched": ner_info.get("skills", []),
            "education": ner_info.get("education", []),
            "experience_years": ner_info.get("years_experience"),
        })
        
    # 3. Sort candidates by final score descending and assign rank (1 to N)
    ranked_outputs = rank_candidates(raw_outputs)
    
    # 4. Form final payload
    final_outputs = []
    for item in ranked_outputs:
        final_outputs.append({
            "rank": item["rank"],
            "filename": item["filename"],
            "tfidf_score": item["tfidf_score"],
            "sbert_score": item["sbert_score"],
            "final_score": item["final_score"],
            "missing_keywords": item["missing_keywords"],
            "skills_matched": item["skills_matched"],
            "education": item["education"],
            "experience_years": item["experience_years"]
        })
        
    return final_outputs
