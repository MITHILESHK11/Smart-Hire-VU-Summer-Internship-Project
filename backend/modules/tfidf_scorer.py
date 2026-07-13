from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

def compute_tfidf_similarity(jd_text: str, resume_texts: List[str]) -> List[float]:
    """
    Computes TF-IDF cosine similarity between a job description and a list of resumes.
    Returns a list of scores (floats between 0.0 and 1.0).
    """
    if not resume_texts:
        return []
        
    # Combine job description and all resumes into one corpus for vectorizer training
    corpus = [jd_text] + resume_texts
    
    # Configure vectorizer as specified: unigrams and bigrams, max 5000 features
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        stop_words=None  # Stop words already removed in preprocessing step
    )
    
    try:
        # Fit and transform the corpus
        tfidf_matrix = vectorizer.fit_transform(corpus)
        
        # JD is the first document (index 0)
        jd_vector = tfidf_matrix[0:1]
        
        # Resumes are from index 1 onwards
        resumes_matrix = tfidf_matrix[1:]
        
        # Compute cosine similarity
        similarities = cosine_similarity(resumes_matrix, jd_vector).flatten()
        
        # Return as list of floats
        return [float(score) for score in similarities]
        
    except Exception as e:
        # Graceful fallback: return 0.0 if vectorizer fails (e.g. empty inputs)
        return [0.0] * len(resume_texts)
