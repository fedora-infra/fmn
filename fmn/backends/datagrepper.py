import logging
from typing import Any, AsyncIterator

from httpx import AsyncClient

from ..core.util import make_synchronous
from .base import APIClient, NextPageParams

log = logging.getLogger(__name__)


class DatagrepperAsyncProxy(APIClient):
    """Proxy for the Datagrepper API endpoints used in FMN"""

    API_VERSION = "v2"

    payload_field = "raw_messages"

    def __init__(self, base_url: str):
        self.client = AsyncClient(
            base_url=f"{base_url.rstrip('/')}/{self.API_VERSION}", timeout=None
        )

    def determine_next_page_params(self, url: str, params: dict, result: dict) -> NextPageParams:
        if "arguments" in result and "page" in result["arguments"] and "pages" in result:
            page_number = result["arguments"]["page"]
            if page_number < result["pages"]:
                params["page"] = page_number + 1
                return url, params

        return None, None

    async def search(self, **params: dict[str, Any]) -> AsyncIterator[dict]:
        async for msg in self.get_paginated("/search", params=params):
            yield msg


DatagrepperSyncProxy = make_synchronous(DatagrepperAsyncProxy, name="DatagrepperSyncProxy")
