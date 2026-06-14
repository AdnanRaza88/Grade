from fastapi import APIRouter
from app.ai import get_health_tip

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/health-tips")
def health_tips():
    tip = get_health_tip()
    return {"tip": tip}