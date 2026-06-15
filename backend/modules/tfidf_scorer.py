# tfidf_scorer.py
# Module 4A: TF-IDF Scoring Engine

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def build_tfidf_matrix(documents: list[str]):
    """Builds a TF-IDF matrix for a list of preprocessed document strings."""
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
    matrix = vectorizer.fit_transform(documents)
    return vectorizer, matrix

def compute_tfidf_similarity(jd_text: str, resume_texts: list[str]) -> list[float]:
    """Computes TF-IDF cosine similarity between the job description and a list of resumes."""
    if not resume_texts:
        return []
    
    # Normalize None and empty/whitespace-only texts to empty strings
    cleaned_jd = jd_text if (jd_text and jd_text.strip()) else ""
    cleaned_resumes = [r if (r and r.strip()) else "" for r in resume_texts]
    
    # Combine job description and resumes into a single corpus to build vocabulary
    all_docs = [cleaned_jd] + cleaned_resumes
    vectorizer, matrix = build_tfidf_matrix(all_docs)
    
    jd_vector = matrix[0]
    resume_vectors = matrix[1:]
    
    # Calculate cosine similarity between JD vector and each resume vector
    similarities = cosine_similarity(jd_vector, resume_vectors)[0]
    return [float(score) for score in similarities]


def get_top_tfidf_keywords(jd_text: str, top_n=20) -> list[str]:
    """Extracts top TF-IDF weighted terms from the job description for gap analysis."""
    if not jd_text or not jd_text.strip():
        return []
        
    # Standard English stop words excluded to filter out noise
    vectorizer = TfidfVectorizer(ngram_range=(1, 1), stop_words="english")
    try:
        matrix = vectorizer.fit_transform([jd_text])
        feature_names = vectorizer.get_feature_names_out()
        scores = matrix.toarray()[0]
        
        # Sort feature names by score descending
        sorted_indices = np.argsort(scores)[::-1]
        top_keywords = [feature_names[i] for i in sorted_indices[:top_n]]
        return top_keywords
    except Exception:
        # Graceful fallback to simple word token extraction if sklearn vectorizer raises empty vocabulary
        words = [w.lower() for w in jd_text.split() if len(w) > 2]
        return list(set(words))[:top_n]
