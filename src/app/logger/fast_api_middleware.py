import uuid
from typing import Callable, Awaitable

from .context_vars import request_id_ctx
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

REQUEST_ID_KEY = "request_id"

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = request.headers.get(REQUEST_ID_KEY, str(uuid.uuid4()))

        request_id_ctx.set(request_id)

        response = await call_next(request)
        response.headers["request_id"] = request_id
        return response
