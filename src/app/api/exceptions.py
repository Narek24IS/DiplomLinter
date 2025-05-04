from typing import Any, Sequence

from fastapi import status as http_status


class ApiException(Exception):
    default_status: int = http_status.HTTP_500_INTERNAL_SERVER_ERROR
    default_error: str = "Oops! Something goes wrong"

    def __init__(
        self,
        status: int | None = None,
        error: str | None = None,
        payload: dict | Sequence | None = None,
        debug: Any = None,
    ):
        self._status = status if status else self.default_status
        self._error = error if error else self.default_error
        self._payload = payload
        self._debug = debug

    @property
    def status(self) -> int:
        return self._status

    @property
    def error(self) -> str:
        return self._error

    @property
    def payload(self) -> dict | Sequence | None:
        return self._payload

    @property
    def debug(self) -> Any:
        return self._debug

    @classmethod
    def code(cls):
        return cls.__name__

    def to_dict(self) -> dict:
        return {
            "code": self.code(),
            "error": self.error,
            "payload": self.payload,
            "debug": self.debug,
        }


class ApiValidationError(ApiException):
    default_status = http_status.HTTP_422_UNPROCESSABLE_ENTITY
