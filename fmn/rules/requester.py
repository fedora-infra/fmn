import logging
from typing import TYPE_CHECKING

from .services.distgit import DistGitService
from .services.fasjson import FasjsonService

if TYPE_CHECKING:
    from fedora_messaging.message import Message


log = logging.getLogger(__name__)


class Requester:
    def __init__(self, config):
        self.distgit = DistGitService(config.distgit_url)
        self.fasjson = FasjsonService(config.fasjson_url)

    async def invalidate_on_message(self, message: "Message"):
        await self.distgit.invalidate_on_message(message)
        await self.fasjson.invalidate_on_message(message)
