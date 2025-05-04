from fastapi import APIRouter

from app.api.technical import router as technical_router

__all__ = ("router",)

router = APIRouter()
router.include_router(technical_router, prefix="/technical", tags=["technical"])
