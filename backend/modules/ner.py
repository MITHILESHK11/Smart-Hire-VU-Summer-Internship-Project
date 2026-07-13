import re
import spacy
from typing import List, Dict, Any, Tuple

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = spacy.load("en_core_web_sm")

# Curated list of technical skills and categories
TECH_SKILLS = [
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go", "rust", "php", "swift", "kotlin", "scala", "r", "sql", "html", "css", "bash",
    # Frameworks & Libraries
    "react", "angular", "vue", "node", "django", "flask", "fastapi", "spring boot", "next.js", "express", "laravel", "rails", "jquery", "bootstrap", "tailwind",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy", "opencv", "nltk", "spacy", "huggingface", "transformers", "d3.js", "three.js",
    # Databases & Caching
    "mysql", "postgresql", "postgres", "mongodb", "sqlite", "redis", "elasticsearch", "cassandra", "mariadb", "oracle", "dynamodb",
    # Cloud & DevOps
    "aws", "amazon web services", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s", "git", "github", "gitlab", "jenkins", "terraform", "ansible",
    "ci/cd", "prometheus", "grafana", "nginx", "apache", "linux",
    # Concepts
    "machine learning", "deep learning", "nlp", "natural language processing", "computer vision", "artificial intelligence", "ai",
    "data science", "data analysis", "agile", "scrum", "rest api", "graphql", "microservices", "system design", "oop", "object oriented programming"
]

# Common educational degrees and variations
DEGREE_PATTERNS = [
    r"\bph\.?d\b",
    r"\bm\.?s\.?c\b",
    r"\bb\.?s\.?c\b",
    r"\bm\.?tech\b",
    r"\bb\.?tech\b",
    r"\bb\.?e\b",
    r"\bm\.?e\b",
    r"\bm\.?b\.?a\b",
    r"\bm\.?c\.?a\b",
    r"\bb\.?c\.?a\b",
    r"\bmaster(?:'s)?\s+(?:of\s+)?(?:science|arts|engineering|technology|business|computer applications|science in computer science|sc)\b",
    r"\bbachelor(?:'s)?\s+(?:of\s+)?(?:science|arts|engineering|technology|business|computer applications|science in computer science|sc)\b",
    r"\bb\.?s\b",
    r"\bm\.?s\b",
    r"\bb\.?a\b",
    r"\bm\.?a\b",
    r"\bdegree in\s+\w+\b"
]

# Common Job Titles
JOB_TITLES = [
    "software engineer", "software developer", "frontend engineer", "frontend developer", "backend engineer", "backend developer",
    "full stack engineer", "full stack developer", "data scientist", "data analyst", "machine learning engineer", "ml engineer",
    "devops engineer", "cloud architect", "system administrator", "database administrator", "qa engineer", "quality assurance engineer",
    "project manager", "product manager", "scrum master", "technical lead", "tech lead", "solution architect", "business analyst"
]

def extract_skills(text: str) -> List[str]:
    """Extracts predefined technical skills from text using sub-string matching."""
    text_lower = text.lower()
    matched_skills = []
    
    # We want to match whole words or specific symbols like C++ and C#
    for skill in TECH_SKILLS:
        # Create regex to match skill as a separate word, handling special characters like +, #
        escaped_skill = re.escape(skill)
        # If the skill ends with a word character, require word boundary. Same for start.
        # But if it ends with '+' or '#', do not require a word boundary on that side.
        pattern = r""
        if skill[0].isalnum():
            pattern += r"\b"
        pattern += escaped_skill
        if skill[-1].isalnum():
            pattern += r"\b"
            
        if re.search(pattern, text_lower):
            # Normalise representation
            matched_skills.append(skill.upper() if len(skill) <= 4 else skill.title())
            
    return sorted(list(set(matched_skills)))

def extract_education(text: str) -> List[str]:
    """Extracts educational qualifications using regex pattern matching."""
    text_lower = text.lower()
    matched_degrees = []
    
    for pattern in DEGREE_PATTERNS:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            # Cleanup and normalize
            match_clean = match.strip().upper()
            if "BACHELOR" in match_clean or "B.E" in match_clean or "B.TECH" in match_clean or "B.S" in match_clean:
                matched_degrees.append("Bachelor's Degree")
            elif "MASTER" in match_clean or "M.E" in match_clean or "M.TECH" in match_clean or "M.S" in match_clean or "MCA" in match_clean or "MBA" in match_clean:
                matched_degrees.append("Master's Degree")
            elif "PH" in match_clean or "DOCTOR" in match_clean:
                matched_degrees.append("PhD")
            else:
                matched_degrees.append(match.title())
                
    return sorted(list(set(matched_degrees)))

def extract_job_titles(text: str) -> List[str]:
    """Extracts job titles from the text."""
    text_lower = text.lower()
    matched_titles = []
    
    for title in JOB_TITLES:
        pattern = r"\b" + re.escape(title) + r"\b"
        if re.search(pattern, text_lower):
            matched_titles.append(title.title())
            
    return sorted(list(set(matched_titles)))

def infer_years_of_experience(text: str) -> float:
    """
    Infers years of experience by:
    1. Looking for explicit patterns (e.g. '5+ years of experience', '3 years of experience').
    2. Looking for date ranges (e.g. '2015 - 2020', 'Jan 2018 to Present') and summing them up.
    Returns the estimated years as a float.
    """
    text_lower = text.lower()
    
    # 1. Look for explicit mentions
    # e.g., "5+ years of experience", "3.5 years of experience", "10 years experience"
    exp_patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+(?:of\s+)?experience",
        r"(\d+(?:\.\d+)?)\+?\s*yrs?\s+(?:of\s+)?experience",
        r"experience\s*(?:of\s*)?:\s*(\d+(?:\.\d+)?)\+?\s*years?",
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+in\s+"
    ]
    
    for pattern in exp_patterns:
        matches = re.findall(pattern, text_lower)
        if matches:
            try:
                # Return the maximum explicit experience found
                return max(float(m) for m in matches)
            except ValueError:
                pass
                
    # 2. Estimate from date ranges
    # E.g., "2018 - 2022", "2015 to 2019", "january 2020 - present", "feb 2021 to current"
    # Find years in format like "20XX" or "19XX"
    # Let's search for "20\d{2}" or "19\d{2}"
    # Date range pattern: (Year1) to/and/dash (Year2 or "present"/"current"/"now")
    date_range_pattern = r"\b(19\d{2}|20\d{2})\s*(?:\-|to|until)\s*(19\d{2}|20\d{2}|present|current|now)\b"
    ranges = re.findall(date_range_pattern, text_lower)
    
    total_years = 0.0
    current_year = 2026 # Context says current time is 2026
    
    for start, end in ranges:
        try:
            start_yr = int(start)
            if end in ["present", "current", "now"]:
                end_yr = current_year
            else:
                end_yr = int(end)
            
            diff = end_yr - start_yr
            if 0 < diff <= 45: # Realistic range for a single job/degree
                total_years += diff
        except ValueError:
            continue
            
    if total_years > 0:
        return min(total_years, 40.0) # Cap at 40 years of experience
        
    return 0.0

def run_ner(text: str) -> Dict[str, Any]:
    """Runs the full NER pipeline to extract all relevant profile structures."""
    return {
        "skills": extract_skills(text),
        "education": extract_education(text),
        "job_titles": extract_job_titles(text),
        "years_of_experience": infer_years_of_experience(text)
    }
