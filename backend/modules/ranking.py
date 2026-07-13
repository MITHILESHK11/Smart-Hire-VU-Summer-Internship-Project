from typing import List, Dict, Any

def compute_keyword_gap(jd_skills: List[str], candidate_skills: List[str]) -> List[str]:
    """
    Computes the keyword gap by identifying required skills from the job description
    that are not present in the candidate's resume.
    """
    jd_skills_lower = {s.lower() for s in jd_skills}
    candidate_skills_lower = {s.lower() for s in candidate_skills}
    
    missing_lower = jd_skills_lower - candidate_skills_lower
    
    # Return the missing skills retaining their original casing from the JD
    return [skill for skill in jd_skills if skill.lower() in missing_lower]

def rank_candidates(
    candidates_data: List[Dict[str, Any]], 
    jd_skills: List[str]
) -> List[Dict[str, Any]]:
    """
    Ranks the list of candidate results based on the hybrid final score.
    Computes missing keyword gaps and matched skills.
    
    candidates_data: list of dicts, each containing:
      - filename: str
      - tfidf_score: float
      - sbert_score: float
      - final_score: float
      - skills: list of str (extracted candidate skills)
      - education: list of str
      - job_titles: list of str
      - years_of_experience: float
    """
    ranked_list = []
    
    for cand in candidates_data:
        cand_skills = cand.get("skills", [])
        missing_skills = compute_keyword_gap(jd_skills, cand_skills)
        matched_skills = [s for s in cand_skills if s.lower() in {js.lower() for js in jd_skills}]
        
        cand_enriched = {
            **cand,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
        }
        ranked_list.append(cand_enriched)
        
    # Sort candidates by final score descending (Python's Timsort is stable, maintaining tie-breaker based on original order)
    ranked_list.sort(key=lambda x: x["final_score"], reverse=True)
    
    # Assign ranks
    for index, cand in enumerate(ranked_list):
        cand["rank"] = index + 1
        
    return ranked_list
