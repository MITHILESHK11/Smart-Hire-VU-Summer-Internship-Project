# ner.py
# Module 3: Named Entity Recognition and Information Extraction

import re
import spacy
from backend.modules.preprocessing import load_nlp_model

# Target vocabulary lists for heuristics and keyword extraction
SKILLS_LIST = [
    "python", "java", "javascript", "typescript", "c++", "c#", "rust", "go", "ruby", "php", "swift", "kotlin",
    "html", "css", "sql", "nosql", "mongodb", "postgresql", "mysql", "redis", "oracle", "sqlite",
    "react", "angular", "vue", "next.js", "node.js", "express", "fastapi", "django", "flask", "spring boot",
    "docker", "kubernetes", "aws", "azure", "gcp", "git", "github", "ci/cd", "jenkins", "terraform", "ansible",
    "spark", "hadoop", "pandas", "numpy", "scikit-learn", "tensorflow", "keras", "pytorch", "spacy", "nltk",
    "bert", "llm", "sbert", "nlp", "machine learning", "deep learning", "artificial intelligence", "agile", "scrum"
]

JOB_TITLES_LIST = [
    "software engineer", "software developer", "frontend engineer", "frontend developer", "backend engineer",
    "backend developer", "fullstack engineer", "fullstack developer", "devops engineer", "cloud architect",
    "system administrator", "database administrator", "dba", "data scientist", "data analyst",
    "machine learning engineer", "ml engineer", "product manager", "project manager", "tech lead",
    "technical lead", "engineering manager", "qa engineer", "quality assurance", "scrum master"
]

EDUCATION_DEGREES = [
    "b.e.", "b.tech", "m.tech", "b.s.", "m.s.", "bsc", "msc", "phd", "ph.d", "mba", "bca", "mca",
    "bachelor", "master", "doctorate", "diploma", "associate degree"
]

def extract_entities(text: str) -> dict:
    """Extracts skills, job titles, education, and years of experience from resume/text."""
    if not text or not text.strip():
        return {
            "skills": [],
            "job_titles": [],
            "education": [],
            "years_experience": None
        }
        
    nlp = load_nlp_model()
    doc = nlp(text)
    
    text_lower = text.lower()
    skills = []
    
    # 1. Extract Skills (Keyword Matching with custom boundaries for symbols like C++)
    for skill in SKILLS_LIST:
        escaped_skill = re.escape(skill)
        if skill.endswith("+") or skill.endswith(".js"):
            # Boundary handling for non-word chars like + or .js
            pattern = rf"\b{escaped_skill}(?:\b|\s|$)"
        else:
            pattern = rf"\b{escaped_skill}\b"
            
        if re.search(pattern, text_lower):
            skills.append(skill)
            
    # 2. Extract Job Titles
    job_titles = []
    for title in JOB_TITLES_LIST:
        pattern = rf"\b{re.escape(title)}\b"
        if re.search(pattern, text_lower):
            job_titles.append(title)
            
    # 3. Extract Education (Degrees + Academic Institutions)
    education = []
    for deg in EDUCATION_DEGREES:
        escaped_deg = re.escape(deg)
        pattern = rf"\b{escaped_deg}\b"
        if re.search(pattern, text_lower):
            education.append(deg)
            
    # Extract ORG entities from spaCy that correspond to academic organizations
    for ent in doc.ents:
        if ent.label_ == "ORG":
            ent_text = ent.text.strip()
            ent_lower = ent_text.lower()
            if any(kw in ent_lower for kw in ["university", "college", "institute", "academy", "school"]):
                if ent_text not in education:
                    education.append(ent_text)
                    
    # 4. Extract Years of Experience
    # Handles: "5 years of experience", "3+ yrs exp", "experience: 2 years", "10 years in software development"
    exp_patterns = [
        r"(?i)\b(\d{1,2})\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp|work|industry|professional)?\b",
        r"(?i)\b(?:experience|exp)\s*(?:of)?\s*(\d{1,2})\+?\s*(?:years?|yrs?)\b"
    ]
    
    years = []
    for pattern in exp_patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            try:
                years.append(int(m))
            except ValueError:
                pass
                
    years_experience = max(years) if years else None
    
    return {
        "skills": sorted(list(set(skills))),
        "job_titles": sorted(list(set(job_titles))),
        "education": sorted(list(set(education))),
        "years_experience": years_experience
    }

def extract_jd_requirements(jd_text: str) -> dict:
    """Extracts required skills, experience, and education from a job description text."""
    return extract_entities(jd_text)
