# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
from unittest.mock import AsyncMock, Mock, call

import pytest
from irc.client import Event

from fmn.sender.handler import HandlerError
from fmn.sender.irc import IRCHandler


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


@pytest.fixture
def handler(mocker, transport):
    aio_factory = AsyncMock(return_value=(transport, Mock()))
    mocker.patch("fmn.sender.irc.AioFactory", return_value=aio_factory)
    handler = IRCHandler({"irc_url": "ircs://username:password@irc.example.com:6697"})
    handler._client.connection.transport = transport
    return handler


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

    transport.write.assert_called_with(b"QUIT :FMN is shutting down\r\n")
    transport.close.assert_called_with()


async def test_irc_handle(transport, handler):
    await handler.handle({"to": "target", "message": "This is a test"})
    transport.write.assert_called_once_with(b"PRIVMSG target :This is a test\r\n")


async def test_irc_nickname_in_use(handler):
    _send_event(
        handler, transport, "nicknameinuse", "server", "user", ["username", "nickname in use"]
    )
    with pytest.raises(HandlerError):
        await handler.setup()


@pytest.mark.parametrize("error_type", ["error", "disconnect"])
async def test_irc_error_not_connected(handler, error_type):
    _send_event(handler, transport, error_type, "server", "user", ["dummy error"])
    with pytest.raises(asyncio.exceptions.CancelledError):
        await handler.setup()


@pytest.mark.parametrize("error_type", ["error", "disconnect"])
async def test_irc_error_while_connected(handler, error_type):
    _send_event(handler, transport, "900", "server", "user")
    await handler.setup()
    _send_event(handler, transport, error_type, "server", "user", ["dummy error"])
    await handler.closed


async def test_irc_disconnect_expected(handler):
    _send_event(handler, transport, "900", "server", "user")
    await handler.setup()
    await handler.stop()
    # We didn't call the shutdown handler
    assert not handler.closed.done()


async def test_irc_disconnect_not_connected(handler):
    handler._client.connected = False
    await handler.stop()
    # We didn't call the shutdown handler
    assert not handler.closed.done()
