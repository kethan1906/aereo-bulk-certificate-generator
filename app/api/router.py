"""Combines all route modules under the /api/v1 prefix."""

from fastapi import APIRouter

from app.api.routes import certificates, generation_jobs

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(generation_jobs.router)
api_router.include_router(certificates.router)
