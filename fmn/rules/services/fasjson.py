from typing import TYPE_CHECKING

from ...backends import FASJSONSyncProxy
from ..cache import cache

if TYPE_CHECKING:
    from fedora_messaging.message import Message


class FasjsonService:
    def __init__(self, url):
        self.url = url
        self.fasjson_proxy = FASJSONSyncProxy(self.url)

    @cache.cache_on_arguments()
    def get_user_groups(self, name: str):
        return [g["groupname"] for g in self.fasjson_proxy.get_user_groups(username=name)]

    def invalidate_on_message(self, message: "Message"):
        if message.topic.endswith("fas.group.member.sponsor"):
            self.get_user_groups.refresh(self, message.body["user"])
            cache.invalidate_tracked()
