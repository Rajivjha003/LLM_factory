from fastapi import APIRouter
from src.llm_ops.core.config import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.app.app_name}

@router.get("/version")
async def version_check():
    return {"version": "0.1.0"}
