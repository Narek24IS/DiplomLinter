from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


def _get_version() -> str:
    try:
        with open(f"{(Path(__file__).parents[1] / 'VERSION').resolve()}", "r") as v:
            version: str = v.read().strip()
    except FileNotFoundError:
        return "0.0.0"
    return version


class Settings(BaseSettings):
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_reload: bool = False
    app_debug: bool = False
    app_version: str = Field(default_factory=_get_version)
    app_environment: str = "local"
    is_access_logs_enabled: bool = False
    base_path: str = ""

    # lint
    lint_wait_timeout: int = 60 * 15
    time_between_checks: int = 10

    # db
    db_username: str = "root"
    db_password: str = "root"
    db_host: str = "database"
    db_port: int = 5432
    db_name: str = "linter"

    # rmq
    rmq_dsn: str = "amqp://guest:guest@rabbitmq:5672/"
    # request queue
    rmq_req_queue: str = "default_req_queue"
    rmq_req_exchange: str = "default_req_exchange"
    rmq_req_routing_key: str = "default_req_routing_key"
    rmq_req_dlx: str = "default_req_dlx"
    rmq_req_retry_count: int = 1
    rmq_req_prefetch_count: int = 1
    # result queue
    rmq_res_exchange: str = "default_res_exchange"
    rmq_res_routing_key: str = "default_res_routing_key"
    rmq_res_retry_count: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
