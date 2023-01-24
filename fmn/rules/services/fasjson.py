import logging
from typing import TYPE_CHECKING

from cashews import cache

from ...backends import FASJSONAsyncProxy
from ...cache.tracked import TrackedCache
from .utils import handle_http_error, normalize_url

if TYPE_CHECKING:
    from fedora_messaging.message import Message


log = logging.getLogger(__name__)


class FasjsonService:
    def __init__(self, url):
        self.url = normalize_url(url)
        self.fasjson_proxy = FASJSONAsyncProxy(self.url)

    @cache(ttl="6h", prefix="v1")
    @handle_http_error(list)
    async def get_user_groups(self, name: str):
        log.debug(f"Getting groups of user {name}")
        return [g["groupname"] for g in await self.fasjson_proxy.get_user_groups(username=name)]

    async def invalidate_on_message(self, message: "Message"):
        if message.topic.endswith("fas.group.member.sponsor"):
            await self._on_permission_change(message.body["user"])

    async def _on_permission_change(self, username):
        await cache.invalidate_func(self.get_user_groups, {"name": username})
        tracked_cache = TrackedCache()
        await tracked_cache.invalidate()
