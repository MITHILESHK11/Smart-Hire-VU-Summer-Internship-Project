# preprocessing.py
# Module 2: NLP Preprocessing Pipeline

import spacy
import re

_nlp = None

def load_nlp_model():
    """Singleton pattern to load spaCy model once into memory."""
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except Exception:
            import spacy.cli
            spacy.cli.download("en_core_web_sm")
            _nlp = spacy.load("en_core_web_sm")
    return _nlp

def clean_text(text: str) -> str:
    """Converts to lowercase, removes special characters, and normalizes whitespace."""
    if not text:
        return ""
    # Lowercase
    cleaned = text.lower()
    # Replace special characters with spaces (preserving alphanumeric)
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', ' ', cleaned)
    # Normalize multiple whitespace down to single space
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def tokenise(text: str) -> list[str]:
    """Tokenizes text using spaCy, removing whitespace tokens."""
    if not text:
        return []
    nlp = load_nlp_model()
    doc = nlp(text)
    return [token.text for token in doc if not token.is_space]

def remove_stopwords(tokens: list[str]) -> list[str]:
    """Removes standard English stopwords using spaCy's built-in stop words list."""
    if not tokens:
        return []
    nlp = load_nlp_model()
    stop_words = nlp.Defaults.stop_words
    return [t for t in tokens if t not in stop_words]

def lemmatise(tokens: list[str]) -> list[str]:
    """Converts a list of token strings into their normalized base/lemma forms using spaCy."""
    if not tokens:
        return []
    nlp = load_nlp_model()
    # Re-assemble tokens into a string for contextual pos-tagging and lemmatization
    doc = nlp(" ".join(tokens))
    return [token.lemma_ for token in doc if not token.is_space]

def preprocess(text: str) -> dict:
    """Chains all preprocessing steps: clean -> tokenize -> remove stopwords -> lemmatize."""
    if not text or not text.strip():
        return {
            "raw": text if text is not None else "",
            "cleaned": "",
            "tokens": [],
            "lemmas": []
        }
        
    cleaned = clean_text(text)
    tokens = tokenise(cleaned)
    no_stopwords = remove_stopwords(tokens)
    lemmas = lemmatise(no_stopwords)
    
    return {
        "raw": text,
        "cleaned": cleaned,
        "tokens": tokens,
        "lemmas": lemmas
    }
