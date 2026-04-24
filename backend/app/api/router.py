from fastapi import APIRouter

from app.api.routers import analysis, health, policies, repositories

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(repositories.router)
api_router.include_router(policies.router)
api_router.include_router(analysis.router)
