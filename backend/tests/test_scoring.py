# test_scoring.py
# Unit Tests for Phase 3 Scoring Engine and Ranking

import pytest
from backend.modules.tfidf_scorer import compute_tfidf_similarity
from backend.modules.sbert_scorer import compute_sbert_similarity
from backend.modules.hybrid_scorer import compute_hybrid_scores
from backend.modules.ranking import rank_candidates, compute_keyword_gap

def test_tfidf_scorer_returns_float_0_to_1():
    """TF-IDF similarity outputs should be floats in the 0.0 to 1.0 range."""
    jd = "Python machine learning developer with Docker."
    resumes = ["Experienced Python developer", "Sales executive", ""]
    scores = compute_tfidf_similarity(jd, resumes)
    assert len(scores) == 3
    for s in scores:
        assert isinstance(s, float)
        assert 0.0 <= s <= 1.0

def test_sbert_scorer_returns_float_0_to_1():
    """SBERT similarity outputs should be floats in the 0.0 to 1.0 range."""
    jd = "Python machine learning developer with Docker."
    resumes = ["Experienced Python developer", "Sales executive", ""]
    scores = compute_sbert_similarity(jd, resumes)
    assert len(scores) == 3
    for s in scores:
        assert isinstance(s, float)
        assert 0.0 <= s <= 1.0

def test_hybrid_scorer_math():
    """Hybrid scoring correctly combines lexical and semantic matching scores at alpha=0.4."""
    jd = "Python developer"
    resumes = ["Python developer", "Java engineer"]
    alpha = 0.4
    
    tfidf_scores = compute_tfidf_similarity(jd, resumes)
    sbert_scores = compute_sbert_similarity(jd, resumes)
    
    hybrid_results = compute_hybrid_scores(jd, resumes, alpha=alpha)
    
    assert len(hybrid_results) == 2
    for idx, item in enumerate(hybrid_results):
        expected_score = round(alpha * tfidf_scores[idx] + (1 - alpha) * sbert_scores[idx], 4)
        assert item["final_score"] == expected_score
        assert item["resume_index"] == idx

def test_ranking_sorts_descending():
    """Candidates are sorted descending by final score with rank indexes assigned."""
    candidates = [
        {"final_score": 0.45, "name": "Resume A"},
        {"final_score": 0.85, "name": "Resume B"},
        {"final_score": 0.65, "name": "Resume C"},
    ]
    ranked = rank_candidates(candidates)
    assert len(ranked) == 3
    assert ranked[0]["name"] == "Resume B"
    assert ranked[0]["rank"] == 1
    assert ranked[1]["name"] == "Resume C"
    assert ranked[1]["rank"] == 2
    assert ranked[2]["name"] == "Resume A"
    assert ranked[2]["rank"] == 3

def test_keyword_gap_analysis():
    """Keyword gap analysis detects missing terms in resume texts correctly."""
    jd_keywords = ["Python", "Docker", "Kubernetes", "FastAPI"]
    resume_text = "I am a Python developer with FastAPI expertise. Docker is also used."
    missing = compute_keyword_gap(jd_keywords, resume_text)
    
    assert "Kubernetes" in missing
    assert "Python" not in missing
    assert "Docker" not in missing
    assert "FastAPI" not in missing

def test_empty_resume_handling():
    """Empty and null resume inputs output zero scores without raising errors."""
    jd = "Python Developer"
    resumes = ["", None]
    
    tfidf_scores = compute_tfidf_similarity(jd, resumes)
    sbert_scores = compute_sbert_similarity(jd, resumes)
    hybrid_results = compute_hybrid_scores(jd, resumes, alpha=0.3)
    
    assert len(tfidf_scores) == 2
    assert len(sbert_scores) == 2
    assert len(hybrid_results) == 2
    
    for score in tfidf_scores:
        assert score == 0.0
    for score in sbert_scores:
        assert score == 0.0
    for res in hybrid_results:
        assert res["final_score"] == 0.0
