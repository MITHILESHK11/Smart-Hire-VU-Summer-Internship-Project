import re
import spacy
import logging

logger = logging.getLogger(__name__)

# Load the spaCy model globally. We load it once at startup.
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    logger.warning(f"Could not load 'en_core_web_sm' from spacy. Trying fallback installation... Error: {e}")
    # Fallback load if needed
    nlp = spacy.load("en_core_web_sm")

def clean_text(text: str) -> str:
    """
    Cleans raw text by:
    - Converting to lowercase
    - Normalizing whitespace and newlines
    - Removing special characters (keeping letters, numbers, and basic punctuation/symbols like +, # for languages like C++, C#)
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Clean up formatting artifacts / replace common separators with spaces
    text = re.sub(r'[\r\n\t]', ' ', text)
    
    # Keep alphanumeric characters, spaces, and tech characters like ++, #, .
    # Let's keep basic punctuation for now but clean up odd symbols
    # A regex to keep standard characters but remove garbage characters:
    text = re.sub(r'[^\w\s\+\#\-\.]', ' ', text)
    
    # Normalize multiple whitespace characters to a single space
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def preprocess_text(text: str) -> str:
    """
    Cleans, tokenizes, removes stop-words, and lemmatizes the text.
    Returns a space-separated string of processed lemmas.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return ""
    
    doc = nlp(cleaned)
    processed_tokens = []
    
    for token in doc:
        # Check if it is a stop-word or punctuation/whitespace
        if not token.is_stop and not token.is_punct and not token.is_space:
            # Keep lemmatized form
            lemma = token.lemma_.strip()
            # Retain non-empty lemmas
            if lemma:
                processed_tokens.append(lemma)
                
    return " ".join(processed_tokens)
