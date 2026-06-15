# ingestion.py
# Module 1: Document Ingestion and Text Extraction

import fitz  # PyMuPDF
import docx
import os
import shutil
import logging
from fastapi import UploadFile
from backend.config import settings

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_path: str) -> str:
    """Extracts raw text from a PDF file using PyMuPDF."""
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_path: str) -> str:
    """Extracts raw text from a DOCX file using python-docx."""
    doc = docx.Document(file_path)
    fullText = []
    
    # Extract text from paragraphs
    for para in doc.paragraphs:
        if para.text.strip():
            fullText.append(para.text)
            
    # Extract text from tables
    for table in doc.tables:
        for row in table.rows:
            row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
            if row_text:
                fullText.append(" | ".join(row_text))
                
    return "\n".join(fullText)

def validate_file(file: UploadFile) -> bool:
    """Validates if file has supported extension, is not empty, and size <= limit."""
    filename = file.filename
    if not filename:
        return False
        
    # Check extension
    ext = os.path.splitext(filename)[1].lower()
    if ext not in [".pdf", ".docx"]:
        return False
        
    # Check size
    try:
        # Seek to the end to get file size
        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        file.file.seek(0)  # Reset pointer to start
        
        if size == 0:
            return False
            
        max_size_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        if size > max_size_bytes:
            return False
    except Exception as e:
        logger.error(f"Error checking file size for {filename}: {e}")
        return False
        
    return True

def save_upload(file: UploadFile, upload_dir: str) -> str:
    """Saves the UploadFile to the target directory and returns the absolute path."""
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path

def process_uploads(files: list[UploadFile], upload_dir: str) -> list[dict]:
    """Processes a list of upload files, extracts text, handles failures gracefully."""
    results = []
    for file in files:
        filename = file.filename
        try:
            if not validate_file(file):
                results.append({
                    "filename": filename,
                    "file_path": None,
                    "raw_text": "",
                    "status": "failed",
                    "error": "Invalid file type (must be .pdf/.docx) or size limit exceeded (max 5MB)."
                })
                continue
                
            file_path = save_upload(file, upload_dir)
            ext = os.path.splitext(filename)[1].lower()
            
            raw_text = ""
            if ext == ".pdf":
                raw_text = extract_text_from_pdf(file_path)
            elif ext == ".docx":
                raw_text = extract_text_from_docx(file_path)
                
            if not raw_text.strip():
                results.append({
                    "filename": filename,
                    "file_path": file_path,
                    "raw_text": "",
                    "status": "failed",
                    "error": "Extraction returned empty content or corrupt file."
                })
                continue
                
            results.append({
                "filename": filename,
                "file_path": file_path,
                "raw_text": raw_text.strip(),
                "status": "success"
            })
        except Exception as e:
            logger.error(f"Error processing upload file {filename}: {e}")
            results.append({
                "filename": filename,
                "file_path": None,
                "raw_text": "",
                "status": "failed",
                "error": f"Internal extraction error: {str(e)}"
            })
            
    return results
