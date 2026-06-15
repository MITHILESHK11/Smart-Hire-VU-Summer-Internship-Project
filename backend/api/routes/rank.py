# rank.py
from fastapi import APIRouter

router = APIRouter(prefix="/rank", tags=["Rank"])

@router.post("")
async def rank_resumes():
    return {"message": "Placeholder for rank endpoint"}
