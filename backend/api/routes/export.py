# export.py
from fastapi import APIRouter

router = APIRouter(prefix="/export", tags=["Export"])

@router.get("/{session_id}")
async def export_results(session_id: str):
    return {"session_id": session_id, "message": "Placeholder for export endpoint"}
