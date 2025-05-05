import json

import aio_pika
from aio_pika import DeliveryMode
from structlog.stdlib import AsyncBoundLogger

from ..dependencies import get_logger

logger: AsyncBoundLogger = get_logger("RabbitPublisher")


class RabbitPublisher:
    def __init__(
        self,
        rmq_dsn: str,
        exchange: str,
        exchange_type: str,
        routing_key: str,
        retry_count: int,
    ):
        self.rmq_dsn = rmq_dsn
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.routing_key = routing_key
        self.retry_count = retry_count
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.rmq_dsn, timeout=10)
        self.channel = await self.connection.channel(publisher_confirms=False)
        await logger.info("Connected to RabbitMQ")

    async def publish(self, message):
        tries = 0
        while True:
            try:
                exchange: aio_pika.Exchange = await self.channel.declare_exchange(
                    name=self.exchange,
                    type=self.exchange_type,
                    durable=True,
                )
                await exchange.publish(
                    aio_pika.Message(
                        body=json.dumps(message).encode(),
                        delivery_mode=DeliveryMode.PERSISTENT,
                    ),
                    routing_key=self.routing_key,
                )
                await logger.info("Published message: {}".format(message))
                return

            except Exception as e:
                if tries >= self.retry_count:
                    raise e

                await logger.warning(f"cannot send message: {e}")

                await self.connect()
                tries += 1

    async def close(self):
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()

    async def is_ready(self) -> bool:
        connection_ready = self.connection and not self.connection.is_closed
        channel_ready = self.channel and not self.channel.is_closed
        return bool(connection_ready and channel_ready)
