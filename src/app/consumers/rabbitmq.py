import asyncio
import time
from asyncio import sleep
from dataclasses import dataclass, field

import aio_pika
from aio_pika.abc import (
    AbstractIncomingMessage,
    AbstractRobustConnection,
    AbstractRobustQueue,
    ExchangeType,
)
from fastapi import FastAPI
from pydantic import ValidationError
from structlog.stdlib import AsyncBoundLogger

from app.consumers.models import ProjectForLint, ProjectLintResult
from app.dependencies import get_logger
from app.linting.linter_runner import start_local_lint
from app.settings import get_settings
from app.tools.urls import ProjectType, convert_url_to_project_name


@dataclass
class RabbitConsumer:
    """
    Класс для обработки сообщений RabbitMQ.

    :param app: Экземпляр FastAPI.
    :param rmq_dsn: DSN для подключения к RabbitMQ.
    :param queue_name: Название очереди, куда приходят запросы на сканирование.
    :param exchange_name: Название exchange, куда привязывается очередь.
    :param dlq_name: Название Dead Letter Queue.
    :param dlx_name: Название Dead Letter Exchange.
    :param routing_key: Ключ для определения нужных сообщений.
    :param max_retries: Максимальное количество попыток обработки сообщений.
    :param logger: Логгер для логирования событий.
    """

    app: FastAPI
    rmq_dsn: str
    queue_name: str
    exchange_name: str
    dlq_name: str
    dlx_name: str
    routing_key: str
    max_retries: int = field(default=1)
    prefetch_count: int = field(default=1)
    logger: AsyncBoundLogger = get_logger("RabbitConsumer")
    connection = None
    channel = None
    queue = None

    async def post_init(self):
        """Настройка соединения и очередей RabbitMQ."""
        await self.logger.info("Initializing RabbitConsumer.")
        loop = asyncio.get_event_loop()
        self.connection: AbstractRobustConnection = await aio_pika.connect_robust(self.rmq_dsn, loop=loop)
        await self.logger.info("Connected to RabbitMQ.")

        self.channel = await self.connection.channel(publisher_confirms=False)
        await self.channel.set_qos(prefetch_count=self.prefetch_count)

        dlx = await self.channel.declare_exchange(self.dlx_name, ExchangeType.DIRECT, durable=True)
        await self.logger.info(f"Declared Dead Letter Exchange: {self.dlx_name}")

        dlq = await self.channel.declare_queue(self.dlq_name, durable=True)
        await dlq.bind(dlx, self.routing_key)
        await self.logger.info(f"Bound Dead Letter Queue: {self.dlq_name}")

        self.queue: AbstractRobustQueue = await self.channel.declare_queue(
            self.queue_name,
            durable=True,
            arguments={
                "x-dead-letter-exchange": self.dlx_name,
                "x-dead-letter-routing-key": self.routing_key,
            },
        )
        await self.queue.bind(self.exchange_name, self.routing_key)
        await self.logger.info(f"Queue {self.queue_name} is bound to exchange {self.exchange_name}.")

        await self.queue.consume(self.process_lint_start_message)

    async def close(self):
        """Закрытие соединения и канала RabbitMQ."""
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
            await self.logger.info("RabbitMQ channel closed.")
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            await self.logger.info("RabbitMQ connection closed.")

    async def is_ready(self) -> bool:
        """
        Проверяет готовность соединения и канала.

        :return: True, если соединение и канал готовы.
        """
        connection_ready = self.connection and not self.connection.is_closed
        channel_ready = self.channel and not self.channel.is_closed
        await self.logger.debug("RabbitConsumer readiness check.")
        return bool(connection_ready and channel_ready)

    async def process_lint_start_message(self, message: AbstractIncomingMessage):
        """
        Обрабатывает входящее сообщение из RabbitMQ.

        :param message: Входящее сообщение.
        """
        await self.logger.info(f"Handling lint start message: Body: {message.body!r}, Headers: {message.headers}")
        sca_url = ""
        try:
            message_data = ProjectForLint.model_validate_json(message.body)
        except ValidationError as e:
            await self.logger.error(f"Can't parse message {message.body!r}", exc_info=e)
            await message.reject(requeue=False)
            return
        project_name = convert_url_to_project_name(message_data.repository_url, ProjectType.CLI)
        try:
            project_id = 1 #TODO
            if project_id is None:
                raise Exception("Can't create or get project ID.")

            await self.start_project_lint(message_data)

            sca_url = ""#TODO
            policy_alerts = ""#TODO

            res = ProjectLintResult(
                task_id=message_data.id,
                repository_url=message_data.repository_url,
                sca_result_url=sca_url,
                error="Policy Alert: Blocker policy alert was found" if policy_alerts else "",
            )
            await self.logger.info(f"[{project_name}] SCA result: {res}")
            await self.app.rabbit_sca_publisher.publish(res.model_dump())  # type: ignore
            await message.ack()
        except Exception as e:
            err_type = type(e).__name__
            fmt_error = f"{err_type} {e}"

            await self.logger.error(
                f"[{project_name}] Unexpected error while processing message {message.body!r}: {fmt_error}",
                exc_info=e,
            )
            await self.app.rabbit_sca_publisher.publish(  # type: ignore
                ProjectLintResult(
                    task_id=message_data.id,
                    repository_url=message_data.repository_url,
                    sca_result_url=sca_url,
                    error=fmt_error,
                ).model_dump()
            )
            await message.reject(requeue=False)

    async def start_project_lint(self, project: ProjectForLint):
        """
        Запускает процесс линтинга проекта и возвращает его результат.

        :param project: Данные проекта для линтинга.
        """
        attempts = 0
        while attempts < self.max_retries:
            try:
                await start_local_lint(project)
                return
            except Exception as e:
                attempts += 1
                await self.logger.warning(
                    f"Attempt {attempts}/{self.max_retries} for lint project "
                    f"{project.repository_url}({project.branch_name}) failed with an error: {e}"
                )
                if attempts >= self.max_retries:
                    await self.logger.warning(
                        f"Failed to process project {project.repository_url}({project.branch_name}) "
                        f"after {self.max_retries} attempts."
                    )
                    raise e
                await asyncio.sleep(3 * attempts)

    async def wait_lint_results(self, project_id: int) -> str:
        """
        Ожидает завершения сканирования проекта и возвращает его результат
        или ошибку таймаута.

        :param project_id: Идентификатор проекта.
        :return: Пустая строка, если сканирование не нашло замечаний и окончилось за 15 минут
        """
        settings = get_settings()
        timeout_at = time.time() + settings.lint_wait_timeout

        while time.time() < timeout_at:
            status = ""#TODO
            await self.logger.debug(f"Code lint status for project with id {project_id}: {status}")

            if status == "":#TODO
                policy_alerts = ""#TODO
                if policy_alerts:
                    return "Policy Alert: Blocker policy alert was found"
                return ""

            await asyncio.sleep(settings.time_between_checks)

        await self.logger.warning(f"Timeout while waiting for lint results for project with id {project_id}")
        raise TimeoutError("The lint didn’t finish in time")
