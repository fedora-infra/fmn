import logging
from collections.abc import Awaitable
from typing import Any

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

    async def get(self, url, **kwargs) -> JSON_RESULT:
        """Query the API and merge paginated results if applicable."""
        params = kwargs.pop("params", {})

        complete_result = None
        partial_result = []

        while complete_result is None:
            response = await self.client.get(url, params=params, **kwargs)
            response.raise_for_status()

            result = response.json()

            if "page" in result:
                partial_result.extend(result["result"])
                page_number = result["page"]["page_number"]
                if page_number < result["page"]["total_pages"]:
                    params["page_number"] = page_number + 1
                else:
                    complete_result = partial_result
            else:
                if partial_result:
                    raise RuntimeError("Can't merge paginated with unpaginated result.")
                complete_result = result["result"]

        return complete_result

    def search_users(self, **kwargs) -> Awaitable[JSON_RESULT]:
        return self.get("/search/users/", **kwargs)

    def get_user(self, *, username: str, **kwargs) -> Awaitable[JSON_RESULT]:
        return self.get(f"/users/{username}/", **kwargs)

    def list_user_groups(self, *, username: str, **kwargs) -> Awaitable[JSON_RESULT]:
        return self.get(f"/users/{username}/groups/", **kwargs)


def get_fasjson_proxy(settings: Settings = Depends(get_settings)) -> FASJSONAsyncProxy:
    return FASJSONAsyncProxy(fasjson_url=settings.services.fasjson_url)
