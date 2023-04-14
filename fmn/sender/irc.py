# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
import logging
from urllib.parse import urlparse

from irc.client import ServerConnectionError
from irc.client_aio import AioSimpleIRCClient
from irc.connection import AioFactory

from .handler import Handler, HandlerError

log = logging.getLogger(__name__)


class IRCHandler(Handler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = IRCClient()

    async def setup(self):
        irc_url = urlparse(self._config["irc_url"])
        await self._client.connect(
            irc_url.hostname,
            irc_url.port,
            irc_url.username,
            password=irc_url.password,
            connect_factory=AioFactory(ssl=(irc_url.scheme == "ircs")),
        )
        log.debug("IRC connection established")

    async def stop(self):
        log.debug("Stopping IRC handler...")
        await self._client.disconnect()

    @property
    def closed(self):
        return self._client.closed

    async def handle(self, message):
        log.info("Sending messsage to %s: %s", message["to"], message["message"])
        await self._client.privmsg(message["to"], message["message"])


class IRCClient(AioSimpleIRCClient):
    _shutdown_message = "FMN is shutting down"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._connection_future = None
        self.closed = asyncio.get_event_loop().create_future()

    async def connect(self, *args, **kwargs):
        self._connection_future = asyncio.Future()
        await self.connection.connect(*args, **kwargs)
        try:
            await self._connection_future
        except asyncio.exceptions.CancelledError:
            self.connection.disconnect("Connection cancelled")
            raise
        except ServerConnectionError as e:
            message = e.args[0]
            self.closed.set_result(message)
            raise HandlerError(f"the handler could not connect: {message}") from e

    async def privmsg(self, *args, **kwargs):
        # This is not async yet.
        return self.connection.privmsg(*args, **kwargs)

    async def disconnect(self):
        if self.connection.connected:
            return self.connection.disconnect(self._shutdown_message)

    def _cancel_or_close(self, message):
        """Cancel or close the futures on shutdown.

        Cancel the ``_connection_future`` if it's not done yet, otherwise set the ``closed``
        future to signal shutdown.

        Args:
            message (str): The message for the cancellation or the closed future result.
        """
        if self._connection_future.done():
            self.closed.set_result(message)
        else:
            # This will disconnect and set the closed future
            self._connection_future.cancel(message)

    def on_disconnect(self, connection, event):
        message = event.arguments[0]
        if message != self._shutdown_message:
            self._cancel_or_close(message)

    def on_error(self, connection, event):
        self._cancel_or_close(event.arguments[0])

    def on_nicknameinuse(self, connection, event):
        message = f"{event.arguments[0]}: {event.arguments[1]}"
        self._connection_future.set_exception(ServerConnectionError(message))

    def on_900(self, connection, event):
        # When logged in.
        # See IRCv3: https://ircv3.net/specs/extensions/sasl-3.1.html#numerics-used-by-this-extension
        self._connection_future.set_result(connection)
