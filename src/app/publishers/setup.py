from aio_pika import ExchangeType
from starlette.requests import Request

from ..publishers.rabbitmq import RabbitPublisher
from ..settings import Settings


def setup_publishers(app, settings: Settings):
    @app.on_event("startup")
    async def on_start():
        rabbit_sca_publisher = RabbitPublisher(
            rmq_dsn=settings.rmq_dsn,
            exchange=settings.rmq_res_exchange,
            exchange_type=ExchangeType.DIRECT,
            routing_key=settings.rmq_res_routing_key,
            retry_count=settings.rmq_res_retry_count,
        )
        await rabbit_sca_publisher.connect()
        app.rabbit_sca_publisher = rabbit_sca_publisher

    @app.on_event("shutdown")
    async def on_shutdown():
        if app.rabbit_sca_publisher:
            await app.rabbit_sca_publisher.close()


async def get_sca_publisher(request: Request) -> RabbitPublisher:
    return request.app.rabbit_sca_publisher
