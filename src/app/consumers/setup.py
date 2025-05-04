from starlette.requests import Request

from app.consumers.rabbitmq import RabbitConsumer
from app.settings import Settings


def setup_consumers(app, settings: Settings):
    @app.on_event("startup")
    async def on_start():
        rabbit_consumer = RabbitConsumer(
            app=app,
            rmq_dsn=settings.rmq_dsn,
            queue_name=settings.rmq_req_queue,
            exchange_name=settings.rmq_req_exchange,
            dlq_name="dlq_" + settings.rmq_req_queue,
            dlx_name=settings.rmq_req_dlx,
            routing_key=settings.rmq_req_routing_key,
            max_retries=settings.rmq_req_retry_count,
            prefetch_count=settings.rmq_req_prefetch_count,
        )
        await rabbit_consumer.post_init()
        app.rabbit_sca_consumer = rabbit_consumer

    @app.on_event("shutdown")
    async def on_shutdown():
        if app.rabbit_sca_consumer:
            await app.rabbit_sca_consumer.close()


async def get_sca_consumer(request: Request) -> RabbitConsumer:
    return request.app.rabbit_sca_consumer
