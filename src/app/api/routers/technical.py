from fastapi import APIRouter, Depends, status
from httpx import Response

from ...consumers.setup import get_sca_consumer
from ...publishers.setup import get_sca_publisher

router = APIRouter(prefix="/technical", tags=["technical"])


@router.get("/ping")
async def ping():
    return Response(status_code=status.HTTP_200_OK, json={"status": "ok"})


@router.get("/ready")
async def ready_check(consumer=Depends(get_sca_consumer), publisher=Depends(get_sca_publisher)):
    """
    Ручка для проверки готовности контейнера.
    :param consumer: Коннект к кролику для обработки сообщений
    :param publisher: Коннект к кролику для публикации сообщений с результатами
    :return: 200 если оба коннекта готовы, 500 в противном случае
    """
    if await consumer.is_ready() and await publisher.is_ready():
        return Response(status_code=status.HTTP_200_OK, json={"status": "ready"})
    return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, json={"status": "not_ready"})
