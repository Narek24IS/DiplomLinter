import uvicorn

from app.settings import get_settings

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "app.app:application",
        host=settings.app_host,
        port=settings.app_port,
        log_level="debug" if settings.app_debug else "info",
        reload=settings.app_reload,
    )
