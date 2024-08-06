# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
import re
from functools import cache as ft_cache
from functools import cached_property as ft_cached_property
from typing import TYPE_CHECKING, Any

import httpx
from cashews import cache
from httpx_gssapi import HTTPSPNEGOAuth

from ..cache.util import cache_ttl
from ..core.config import get_settings
from .base import APIClient, NextPageParams, handle_http_error

if TYPE_CHECKING:
    from fedora_messaging.message import Message
    from sqlalchemy.ext.asyncio import AsyncSession

log = logging.getLogger(__name__)


class FASJSONAsyncProxy(APIClient):
    """Proxy for the FASJSON API endpoints used in FMN"""

    API_VERSION = "v1"

    FAS_TOPIC_RE = re.compile(
        r"fas\.(?P<usergroup>user|group)\.(?P<event>member\.sponsor|create|update)$"
    )

    payload_field = "result"

    def __init__(self, base_url: str) -> None:
        super().__init__(base_url=base_url, auth=HTTPSPNEGOAuth())

    @ft_cached_property
    def api_url(self) -> str:
        return f"{self.base_url.rstrip('/')}/{self.API_VERSION}"

    def determine_next_page_params(self, url: str, params: dict, result: dict) -> NextPageParams:
        if "page" in result and "page_number" in result["page"] and "total_pages" in result["page"]:
            page_number = result["page"]["page_number"]
            if page_number < result["page"]["total_pages"]:
                params["page_number"] = page_number + 1
                return url, params

        return None, None

    @cache(
        ttl=cache_ttl("fasjson"),
        prefix="v1",
        tags=["fasjson:search_users:username__exact={username__exact}"],
    )
    async def search_users(
        self,
        username: str | None = None,
        username__exact: str | None = None,
        **params: dict[str, Any],
    ) -> list[dict]:
        if username:
            params["username"] = username
        if username__exact:
            params["username__exact"] = username__exact
        return [user async for user in self.get_paginated("/search/users/", params=params)]

    @cache(ttl=cache_ttl("fasjson"), prefix="v1", tags=["get_user:username={username}"])
    async def get_user(self, *, username: str) -> dict | None:
        try:
            return await self.get_payload(f"/users/{username}/")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    @handle_http_error(list)
    @cache(ttl=cache_ttl("fasjson"), prefix="v1")
    async def get_user_groups(self, *, username: str) -> dict:
        return await self.get_payload(f"/users/{username}/groups/")

    async def invalidate_on_message(self, message: "Message", db: "AsyncSession") -> None:
        if not self.FAS_TOPIC_RE.search(message.topic):
            # Bail out early
            log.debug("Skipping message with topic %s", message.topic)
            return

        if not (msg_user := message.body.get("msg", {}).get("user")):
            log.warning("No information found about affected user")
            return

        try:
            await cache.delete_tags(
                "fasjson:search_users:username__exact=",
                f"fasjson:search_users:username__exact={msg_user}",
                f"fasjson:get_user:username={msg_user}",
                f"fasjson:get_user_groups:username={msg_user}",
            )
        except Exception as exc:
            log.warning("Deleting cache entries yielded an exception: %s", exc)


@ft_cache
def get_fasjson_proxy() -> FASJSONAsyncProxy:
    return FASJSONAsyncProxy(get_settings().services.fasjson_url)
