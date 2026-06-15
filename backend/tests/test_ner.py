# test_ner.py
# Unit Tests for Module 3 (NER Extraction)

import pytest
from backend.modules.ner import extract_entities, extract_jd_requirements

def test_extract_entities_skills():
    """Skills like Python, React, and AWS are correctly extracted."""
    text = "Experienced Python developer with React and AWS knowledge."
    entities = extract_entities(text)
    assert "python" in entities["skills"]
    assert "react" in entities["skills"]
    assert "aws" in entities["skills"]

def test_extract_entities_education():
    """Degrees and academic institutions are detected."""
    text = "Holds a B.Tech in Computer Science from Stanford University."
    entities = extract_entities(text)
    assert "b.tech" in entities["education"]
    assert "Stanford University" in entities["education"]

def test_extract_entities_experience():
    """Years of experience are parsed from text using patterns."""
    text = "Required: 5+ years of experience as a software developer."
    entities = extract_entities(text)
    assert entities["years_experience"] == 5

def test_extract_entities_experience_alternative():
    """Alternative experience writing formats are parsed."""
    text = "We need someone with experience of 10 yrs."
    entities = extract_entities(text)
    assert entities["years_experience"] == 10

def test_extract_entities_empty():
    """Empty strings or None inputs return default empty arrays and None for years."""
    entities = extract_entities("")
    assert entities["skills"] == []
    assert entities["job_titles"] == []
    assert entities["education"] == []
    assert entities["years_experience"] is None
    
    entities_none = extract_entities(None)
    assert entities_none["skills"] == []
    assert entities_none["job_titles"] == []
    assert entities_none["education"] == []
    assert entities_none["years_experience"] is None

def test_extract_jd_requirements():
    """Job description requirements mapping matches standard entity structure."""
    text = "Looking for a DevOps Engineer with Docker, Kubernetes, and 3 years of exp."
    reqs = extract_jd_requirements(text)
    assert "devops engineer" in reqs["job_titles"]
    assert "docker" in reqs["skills"]
    assert "kubernetes" in reqs["skills"]
    assert reqs["years_experience"] == 3
