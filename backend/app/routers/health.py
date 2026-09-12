from fastapi import APIRouter
from app.core.config import get_settings

router = APIRouter(tags=["Health"])

@router.get("/")
async def root():
    return {"message": "Multi-Agent Research API is running", "docs": "/docs"}


@router.get("/health")
async def health_check():
    settings = get_settings()
    return {
        "status": "healthy",
        "openai_configured": bool(settings.openai_api_key),
        "tavily_configured": bool(settings.tavily_api_key),
    }