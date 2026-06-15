# test_ingestion.py
# Unit Tests for Module 1 (Document Ingestion)

import os
import pytest
from fastapi import UploadFile
from unittest.mock import MagicMock
from backend.modules.ingestion import (
    extract_text_from_pdf,
    extract_text_from_docx,
    validate_file,
    process_uploads
)

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

def test_extract_text_from_pdf():
    """Valid PDF text extraction returns expected content."""
    pdf_path = os.path.join(FIXTURES_DIR, "valid_resume.pdf")
    text = extract_text_from_pdf(pdf_path)
    assert isinstance(text, str)
    assert len(text) > 0
    assert "Mithilesh" in text
    assert "Python" in text

def test_extract_text_from_docx():
    """Valid DOCX text extraction returns expected content."""
    docx_path = os.path.join(FIXTURES_DIR, "valid_resume.docx")
    text = extract_text_from_docx(docx_path)
    assert isinstance(text, str)
    assert len(text) > 0
    assert "Ankita" in text
    assert "React" in text

def test_validate_file_valid_pdf():
    """Valid PDF format is correctly accepted."""
    pdf_path = os.path.join(FIXTURES_DIR, "valid_resume.pdf")
    with open(pdf_path, "rb") as f:
        upload_file = UploadFile(filename="valid_resume.pdf", file=f)
        assert validate_file(upload_file) is True

def test_validate_file_valid_docx():
    """Valid DOCX format is correctly accepted."""
    docx_path = os.path.join(FIXTURES_DIR, "valid_resume.docx")
    with open(docx_path, "rb") as f:
        upload_file = UploadFile(filename="valid_resume.docx", file=f)
        assert validate_file(upload_file) is True

def test_validate_file_oversized():
    """Files exceeding size limit (5MB) are rejected."""
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "large.pdf"
    mock_file.file = MagicMock()
    mock_file.file.tell.return_value = 6 * 1024 * 1024  # Mock size as 6 MB
    assert validate_file(mock_file) is False

def test_validate_file_invalid_type():
    """Unsupported extension file types are rejected."""
    png_path = os.path.join(FIXTURES_DIR, "unsupported.png")
    with open(png_path, "rb") as f:
        upload_file = UploadFile(filename="unsupported.png", file=f)
        assert validate_file(upload_file) is False

def test_corrupt_pdf_handling():
    """Reading a corrupt PDF raises an exception or is handled gracefully."""
    corrupt_path = os.path.join(FIXTURES_DIR, "corrupt.pdf")
    # PyMuPDF should raise a fitz error upon reading corrupt PDF content
    with pytest.raises(Exception):
        extract_text_from_pdf(corrupt_path)

def test_process_uploads_mixed(tmpdir):
    """process_uploads returns correct status and paths for batch files."""
    pdf_path = os.path.join(FIXTURES_DIR, "valid_resume.pdf")
    docx_path = os.path.join(FIXTURES_DIR, "valid_resume.docx")
    png_path = os.path.join(FIXTURES_DIR, "unsupported.png")
    
    with open(pdf_path, "rb") as f1, open(docx_path, "rb") as f2, open(png_path, "rb") as f3:
        u1 = UploadFile(filename="valid_resume.pdf", file=f1)
        u2 = UploadFile(filename="valid_resume.docx", file=f2)
        u3 = UploadFile(filename="unsupported.png", file=f3)
        
        results = process_uploads([u1, u2, u3], str(tmpdir))
        
        assert len(results) == 3
        
        # Valid PDF asserts
        assert results[0]["filename"] == "valid_resume.pdf"
        assert results[0]["status"] == "success"
        assert "Python" in results[0]["raw_text"]
        assert results[0]["file_path"] is not None
        
        # Valid DOCX asserts
        assert results[1]["filename"] == "valid_resume.docx"
        assert results[1]["status"] == "success"
        assert "React" in results[1]["raw_text"]
        assert results[1]["file_path"] is not None
        
        # Invalid PNG asserts
        assert results[2]["filename"] == "unsupported.png"
        assert results[2]["status"] == "failed"
        assert results[2]["file_path"] is None
        assert "Invalid file type" in results[2]["error"]
