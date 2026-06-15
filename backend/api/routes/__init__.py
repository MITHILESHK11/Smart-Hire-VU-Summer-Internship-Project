# __init__.py
from fastapi import APIRouter
from .rank import router as rank_router
from .results import router as results_router
from .export import router as export_router

api_router = APIRouter(prefix="/api")
api_router.include_router(rank_router)
api_router.include_router(results_router)
api_router.include_router(export_router)
