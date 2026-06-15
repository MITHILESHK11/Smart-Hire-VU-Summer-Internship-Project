# validation.py
# Input Validation and Exception Handlers

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Custom exception handler for Starlette/FastAPI HTTPExceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom validation handler formatting Pydantic/FastAPI input errors consistently."""
    errors = exc.errors()
    # Format details into readable single-string summary
    detail_msg = "; ".join([
        f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}" 
        for err in errors
    ])
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": detail_msg,
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Fallback exception handler for unhandled internal failures to avoid server crashes."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    )
