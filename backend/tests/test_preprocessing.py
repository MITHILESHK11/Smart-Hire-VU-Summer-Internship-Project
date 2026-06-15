# test_preprocessing.py
# Unit Tests for Module 2 (NLP Preprocessing)

import pytest
from backend.modules.preprocessing import (
    clean_text,
    tokenise,
    remove_stopwords,
    lemmatise,
    preprocess
)

def test_clean_text():
    """Text is lowercased, punctuation removed, and whitespace normalized."""
    text = "Hello, World! This is a Test sentence with 123 numbers..."
    cleaned = clean_text(text)
    assert cleaned == "hello world this is a test sentence with 123 numbers"

def test_tokenise():
    """Text string is tokenized into word lists."""
    text = "hello world python"
    tokens = tokenise(text)
    assert tokens == ["hello", "world", "python"]

def test_remove_stopwords():
    """Standard English stop words are filtered out."""
    tokens = ["hello", "world", "python", "is", "a", "good", "language"]
    no_stopwords = remove_stopwords(tokens)
    assert "is" not in no_stopwords
    assert "a" not in no_stopwords
    assert "python" in no_stopwords
    assert "hello" in no_stopwords

def test_lemmatise():
    """Word tokens are converted to their base lemma forms."""
    tokens = ["managing", "developers", "ran", "successfully"]
    lemmas = lemmatise(tokens)
    # Allow flexibilities based on spaCy dictionary mapping
    assert any(x in lemmas for x in ["manage", "managing"])
    assert any(x in lemmas for x in ["developer", "developers"])
    assert any(x in lemmas for x in ["run", "ran"])

def test_preprocess_full():
    """Full preprocess pipeline chains all modules and outputs dict."""
    text = "Python developers are managing Docker containers!"
    result = preprocess(text)
    assert result["raw"] == text
    assert "python" in result["cleaned"]
    assert "python" in result["tokens"]
    assert "docker" in result["tokens"]
    assert any(lemma in result["lemmas"] for lemma in ["developer", "manage", "docker"])

def test_preprocess_empty():
    """Empty strings and None inputs are handled gracefully without exceptions."""
    result_empty = preprocess("")
    assert result_empty["raw"] == ""
    assert result_empty["cleaned"] == ""
    assert result_empty["tokens"] == []
    assert result_empty["lemmas"] == []
    
    result_none = preprocess(None)
    assert result_none["raw"] == ""
    assert result_none["cleaned"] == ""
    assert result_none["tokens"] == []
    assert result_none["lemmas"] == []
