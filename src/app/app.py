import structlog
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api import exceptions, router
from app.consumers.setup import setup_consumers
from app.publishers.setup import setup_publishers
from app.settings import Settings
from logger import configure_logger


def get_app() -> FastAPI:
    settings = Settings()

    configure_logger(
        enable_json_logs=settings.app_environment != "local",
        debug=settings.app_debug,
        show_locals=settings.app_environment != "local",
        access_logs=settings.is_access_logs_enabled,
        log_level="DEBUG" if settings.app_debug else "INFO",
    )

    app = FastAPI(
        debug=settings.app_debug,
        title="Super Linter",
        version=settings.app_version,
        root_path=settings.base_path.rstrip("/"),
    )
    app.include_router(router)

    setup_consumers(app, settings)
    setup_publishers(app, settings)

    @app.middleware("http")
    async def logging_middleware(request: Request, call_next) -> Response:
        req_id = request.headers.get("request-id")

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=req_id,
        )

        response: Response = await call_next(request)

        return response

    @app.exception_handler(RequestValidationError)
    async def api_validation_error_handler(_: Request, exc: RequestValidationError):
        error = exceptions.ApiValidationError(
            error=str(exc),
            payload=exc.errors(),
        )
        return JSONResponse(
            status_code=error.status,
            content=error.to_dict(),
        )

    @app.exception_handler(Exception)
    async def base_exception_handler(_: Request, exc: Exception):
        error = exceptions.ApiException(debug=str(exc))
        return JSONResponse(
            status_code=error.status,
            content=error.to_dict(),
        )

    @app.exception_handler(exceptions.ApiException)
    async def api_exception_handler(_: Request, exc: exceptions.ApiException):
        return JSONResponse(
            status_code=exc.status,
            content=exc.to_dict(),
        )

    return app


application = get_app()
