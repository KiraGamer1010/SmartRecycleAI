from fastapi import APIRouter

from app.core.config import get_settings


router = APIRouter()


@router.get("/health")
def system_health() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": "backend",
        "environment": settings.environment,
        "api_version": "v1",
    }
