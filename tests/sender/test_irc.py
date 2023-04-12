# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
from unittest.mock import AsyncMock, Mock, call

import pytest
from irc.client import Event

from fmn.sender.irc import IRCClient, IRCHandler


def _send_event(handler, transport, *event_args):
    async def _send_nickname_in_use():
        await asyncio.sleep(0.5)
        handler._client._dispatcher(transport, Event(*event_args))

    # RUF006 is not an issue here, in tests.
    # https://beta.ruff.rs/docs/rules/asyncio-dangling-task/
    asyncio.create_task(_send_nickname_in_use())  # noqa: RUF006


@pytest.fixture
def transport():
    return Mock(name="transport")


async def test_irc_connect(mocker, transport):
    aio_factory = AsyncMock(return_value=(transport, Mock()))
    aio_factory_class = mocker.patch("fmn.sender.irc.AioFactory", return_value=aio_factory)

    handler = IRCHandler({"irc_url": "ircs://username:password@irc.example.com:6697"})

    # Send the logged in event
    _send_event(handler, transport, "900", "server", "user")
    await handler.setup()

    aio_factory_class.assert_called_once_with(ssl=True)
    aio_factory.assert_called_once()
    assert aio_factory.call_args[0][1] == ("irc.example.com", 6697)
    assert call(b"NICK username\r\n") in transport.write.call_args_list
    assert call(b"PASS password\r\n") in transport.write.call_args_list

    await handler.stop()

    transport.write.assert_called_with(b"QUIT\r\n")
    transport.close.assert_called_with()


async def test_irc_handle():
    handler = IRCHandler({"irc_url": "ircs://username:password@irc.example.com:6697"})
    handler._client = IRCClient()
    transport = handler._client.connection.transport = Mock()

    await handler.handle({"to": "target", "message": "This is a test"})

    transport.write.assert_called_once_with(b"PRIVMSG target :This is a test\r\n")
