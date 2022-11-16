import logging
from typing import Any, AsyncIterator

from fastapi import Depends
from httpx import AsyncClient
from httpx_gssapi import HTTPSPNEGOAuth

from ..core.config import Settings, get_settings

log = logging.getLogger(__name__)

JSON_DICT = dict[str, Any]
JSON_RESULT = list[Any] | JSON_DICT


class FASJSONAsyncProxy:
    """Asynchronous proxy for the FASJSON API endpoints used in FMN"""

    API_VERSION = "v1"

    def __init__(self, fasjson_url: str):
        self.client = AsyncClient(
            base_url=f"{fasjson_url.rstrip('/')}/{self.API_VERSION}",
            auth=HTTPSPNEGOAuth(),
            timeout=None,
        )

    async def get(self, url, **kwargs) -> JSON_DICT:
        """Query the API for a single result."""
        response = await self.client.get(url, **kwargs)
        response.raise_for_status()
        return response.json()

    async def get_result(self, url, **kwargs) -> JSON_RESULT:
        return (await self.get(url, **kwargs))["result"]

    async def get_paginated(self, url, **kwargs) -> AsyncIterator[JSON_DICT]:
        """Query the API and iterate over paginated results if applicable."""
        params = kwargs.pop("params", {})

        while True:
            result = await self.get(url, params=params, **kwargs)
            if "page" not in result:
                raise ValueError("missing pagination metadata")

            for item in result["result"]:
                yield item

            page_number = result["page"]["page_number"]
            if page_number >= result["page"]["total_pages"]:
                return

            params["page_number"] = page_number + 1

    async def search_users(self, **params: dict[str, Any]) -> AsyncIterator[JSON_RESULT]:
        async for user in self.get_paginated("/search/users/", params=params):
            yield user

    async def get_user(self, *, username: str) -> JSON_RESULT:
        return await self.get_result(f"/users/{username}/")

    async def get_user_groups(self, *, username: str) -> JSON_RESULT:
        return await self.get_result(f"/users/{username}/groups/")


def get_fasjson_proxy(settings: Settings = Depends(get_settings)) -> FASJSONAsyncProxy:
    return FASJSONAsyncProxy(fasjson_url=settings.services.fasjson_url)
