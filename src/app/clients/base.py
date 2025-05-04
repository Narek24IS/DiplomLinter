import asyncio
from json import JSONDecodeError
from types import TracebackType
from typing import Mapping, Type

import httpx
from fastapi.exceptions import HTTPException
from structlog.stdlib import AsyncBoundLogger

from app.dependencies import get_logger

logger: AsyncBoundLogger = get_logger("HTTPClient")


class HTTPClient:
    def __init__(self, base_url: str | None = None) -> None:
        self._base_url = base_url
        self._client = httpx.AsyncClient(base_url=base_url or "")

    def __repr__(self) -> str:
        return f"{self._base_url} {super().__repr__()}"

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        await self._client.aclose()

    async def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict | None = None,
        json: Mapping | None = None,
        data: dict | None = None,
        files: dict | None = None,
        params: Mapping | None = None,
        timeout: float = 30.0,
        tries: int = 3,
    ):
        method = method.upper()
        if headers is None:
            headers = {}

        request = self._client.build_request(
            method,
            url,
            json=json,
            data=data,
            files=files,
            params=params,
            headers=headers,
            timeout=timeout,
        )
        while tries:
            try:
                resp = await self._client.send(request)
                if resp.is_error:
                    raise HTTPException(status_code=resp.status_code, detail=resp.text)
                try:
                    return resp.json()
                except JSONDecodeError:
                    return {}
            except Exception as e:
                tries -= 1
                await logger.warning(
                    f"Request failed with an error: {e}; Retries left: {tries} Request: {method} {url} "
                    f"Json: {json}; Data: {data}; Params: {params}"
                )
                if tries == 0:
                    raise e

                await asyncio.sleep(5)

    async def close(self):
        await self._client.aclose()
