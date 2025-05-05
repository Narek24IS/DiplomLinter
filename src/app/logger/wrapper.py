import logging
from contextvars import Context
from typing import Iterable, Callable, Any, Tuple, Dict

import structlog
from structlog.processors import CallsiteParameter
from structlog.stdlib import AsyncBoundLogger
from structlog.typing import Processor

from .context_vars import call_context, request_id_ctx


class CustomAsyncBoundLogger(AsyncBoundLogger):
    """
    Обёртка над стандартным асинхронным логгером,
    которая нужна для сохранения в контекст места вызова лога
    """
    def __init__(
            self,
            logger: logging.Logger,
            processors: Iterable[Processor],
            context: Context,
    ):
        self._sync_processor = structlog.processors.CallsiteParameterAdder(
            parameters=[
                CallsiteParameter.PATHNAME,
                CallsiteParameter.LINENO,
            ],
            additional_ignores=["stdlib", "logger.wrapper"]
        )
        super().__init__(logger, processors, context)

    async def _dispatch_to_sync(
            self,
            meth: Callable[..., Any],
            event: str,
            args: Tuple[Any, ...],
            kw: Dict[str, Any],
    ) -> None:
        params = self._sync_processor(None, "", {})  # type: ignore
        call_context.set(params)  # type: ignore
        current_request_id = request_id_ctx.get()
        if current_request_id:
            kw.setdefault("request_id", current_request_id)
        await super()._dispatch_to_sync(meth, event, args, kw)
        # Сброс контекста после его копирования в контекст лога
        call_context.set(dict())
