from fastapi import APIRouter

from app.api.technical import endpoints

router = APIRouter()
router.include_router(endpoints.ping.router)
router.include_router(endpoints.ready.router)
