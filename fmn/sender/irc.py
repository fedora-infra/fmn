import asyncio
import logging
from urllib.parse import urlparse

from irc.client_aio import AioSimpleIRCClient
from irc.connection import AioFactory

from .handler import Handler

_log = logging.getLogger(__name__)


class IRCHandler(Handler):
    async def setup(self):
        self._client = IRCClient()
        irc_url = urlparse(self._config["irc_url"])
        await self._client.connect(
            irc_url.hostname,
            irc_url.port,
            irc_url.username,
            password=irc_url.password,
            connect_factory=AioFactory(ssl=(irc_url.scheme == "ircs")),
        )
        _log.debug("IRC connection established")

    async def stop(self):
        _log.debug("Stopping IRC handler...")
        await self._client.disconnect()

    async def handle(self, message):
        _log.info("Sending messsage to %s: %s", message["to"], message["message"])
        await self._client.privmsg(message["to"], message["message"])


class IRCClient(AioSimpleIRCClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._connection_future = None

    async def connect(self, *args, **kwargs):
        self._connection_future = asyncio.Future()
        await self.connection.connect(*args, **kwargs)
        await self._connection_future

    async def privmsg(self, *args, **kwargs):
        # This is not async yet.
        return self.connection.privmsg(*args, **kwargs)

    def on_welcome(self, connection, event):
        self._connection_future.set_result(connection)

    async def disconnect(self):
        return self.connection.disconnect()
