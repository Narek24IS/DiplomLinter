import structlog
from .logger import get_async_logger


def get_logger(
    logger_name: str = "",
) -> structlog.stdlib.AsyncBoundLogger:
    return get_async_logger(logger_name)
