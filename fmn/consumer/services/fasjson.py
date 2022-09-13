from fasjson_client import Client
from fedora_messaging.message import Message

from ..cache import cache


class FasjsonService:
    def __init__(self, url):
        self.url = url
        self.fasjson_client = Client(self.url)

    @cache.cache_on_arguments()
    def get_user_groups(self, name: str):
        return [g["groupname"] for g in self.fasjson_client.list_user_groups(username=name).result]

    def invalidate_on_message(self, message: Message):
        if message.topic.endswith("fas.group.member.sponsor"):
            self.get_user_groups.refresh(message.body["user"])
            cache.invalidate_tracked()
