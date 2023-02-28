import logging
from collections.abc import AsyncIterator
from functools import cached_property as ft_cached_property
from typing import Any

from .base import APIClient, NextPageParams

log = logging.getLogger(__name__)


class DatagrepperAsyncProxy(APIClient):
    """Proxy for the Datagrepper API endpoints used in FMN"""

    API_VERSION = "v2"

    payload_field = "raw_messages"

    @ft_cached_property
    def api_url(self) -> str:
        return f"{self.base_url.rstrip('/')}/{self.API_VERSION}"

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
