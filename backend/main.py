import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.db.models import init_db
from backend.api.routes.rank import router as rank_router
from backend.api.routes.results import router as results_router
from backend.api.routes.export import router as export_router

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database on startup
    logger.info("Initializing database...")
    init_db()
    yield
    logger.info("Shutting down backend server...")

app = FastAPI(
    title="AI-Powered Resume Ranking System",
    description="Automatically screens and ranks resumes against a job description using a hybrid TF-IDF (lexical) + SBERT (semantic) model.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers under /api prefix
app.include_router(rank_router, prefix="/api")
app.include_router(results_router, prefix="/api")
app.include_router(export_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "AI-Powered Resume Ranking System API is online.",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
