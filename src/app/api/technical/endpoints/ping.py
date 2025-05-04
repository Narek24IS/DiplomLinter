from fastapi import APIRouter, status
from httpx import Response

router = APIRouter()


@router.get("/ping")
async def ping():
    return Response(status_code=status.HTTP_200_OK, json={"status": "ok"})
