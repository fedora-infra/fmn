import logging
from typing import Any, AsyncIterator

from httpx_gssapi import HTTPSPNEGOAuth

from ..core.util import make_synchronous
from .base import APIClient, NextPageParams

log = logging.getLogger(__name__)


class FASJSONAsyncProxy(APIClient):
    """Proxy for the FASJSON API endpoints used in FMN"""

    API_VERSION = "v1"

    payload_field = "result"

    def __init__(self, base_url: str):
        super().__init__(f"{base_url.rstrip('/')}/{self.API_VERSION}", auth=HTTPSPNEGOAuth())

    def determine_next_page_params(self, url: str, params: dict, result: dict) -> NextPageParams:
        if "page" in result and "page_number" in result["page"] and "total_pages" in result["page"]:
            page_number = result["page"]["page_number"]
            if page_number < result["page"]["total_pages"]:
                params["page"] = page_number + 1
                return url, params

        return None, None

    async def search_users(self, **params: dict[str, Any]) -> AsyncIterator[dict]:
        async for user in self.get_paginated("/search/users/", params=params):
            yield user

    async def get_user(self, *, username: str) -> dict:
        return await self.get_payload(f"/users/{username}/")

    async def get_user_groups(self, *, username: str) -> dict:
        return await self.get_payload(f"/users/{username}/groups/")


FASJSONSyncProxy = make_synchronous(FASJSONAsyncProxy, name="FASJSONSyncProxy")
