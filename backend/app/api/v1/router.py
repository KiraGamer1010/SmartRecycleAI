from fastapi import APIRouter

from app.api.v1.endpoints import health, recycling

api_router = APIRouter()
api_router.include_router(health.router, prefix="/system", tags=["system"])
api_router.include_router(recycling.router, prefix="/recycling", tags=["recycling"])
