from .configure_logger import configure_logger, get_logger, get_async_logger
from .fast_api_middleware import RequestIDMiddleware, REQUEST_ID_KEY
from .context_vars import request_id_ctx

configure_logger()
logger = get_logger()
async_logger = get_async_logger()

__all__ = ["configure_logger", "logger", "async_logger", "get_logger", "get_async_logger",
           "RequestIDMiddleware", "request_id_ctx", "REQUEST_ID_KEY"]
