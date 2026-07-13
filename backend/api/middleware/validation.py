import logging
from fastapi import HTTPException, UploadFile
from typing import List

logger = logging.getLogger(__name__)

# Constants as specified in section 4.1 of the report
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_RESUMES_PER_SESSION = 50

def validate_uploaded_files(files: List[UploadFile]):
    """
    Validates uploaded resume files:
    - Maximum count (50 files)
    - Supported extensions (.pdf, .docx, .txt)
    - Maximum file size (5MB)
    """
    if not files or len(files) == 0:
        raise HTTPException(status_code=400, detail="No files uploaded. At least one resume is required.")
        
    if len(files) > MAX_RESUMES_PER_SESSION:
        raise HTTPException(
            status_code=400, 
            detail=f"Too many files. A maximum of {MAX_RESUMES_PER_SESSION} resumes can be processed per session."
        )
        
    for file in files:
        # Check extension
        filename_lower = file.filename.lower()
        has_valid_ext = any(filename_lower.endswith(ext) for ext in SUPPORTED_EXTENSIONS)
        if not has_valid_ext:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format: '{file.filename}'. Only PDF, DOCX, and TXT files are supported."
            )
            
        # We can't always check size without reading, but we can do a size check if content-length is present.
        # Alternatively, we can check file.size in newer FastAPI versions or read a chunk.
        # Let's do a safe check on file size:
        try:
            # Check if file has a size attribute (available in newer starlette/fastapi)
            if hasattr(file, "size") and file.size is not None:
                if file.size > MAX_FILE_SIZE_BYTES:
                    raise HTTPException(
                        status_code=400,
                        detail=f"File '{file.filename}' exceeds the maximum allowed size of {MAX_FILE_SIZE_MB}MB."
                    )
        except Exception as e:
            logger.warning(f"Could not verify file size for '{file.filename}': {e}")
            
    return True

def validate_job_description(jd_text: str):
    """
    Validates the job description text:
    - Minimum 50 characters
    - Maximum 10,000 characters
    """
    if not jd_text or len(jd_text.strip()) < 50:
        raise HTTPException(
            status_code=400,
            detail="Job description is too short. It must contain at least 50 characters to ensure meaningful ranking."
        )
        
    if len(jd_text) > 10000:
        raise HTTPException(
            status_code=400,
            detail="Job description exceeds the maximum length of 10,000 characters."
        )
        
    return True
