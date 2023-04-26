# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
import sys
from unittest.mock import AsyncMock, Mock, call

import pytest
from irc.client import Event

from fmn.sender.handler import HandlerError
from fmn.sender.irc import IRCHandler


def _send_event(handler, transport, *event_args):
    async def _do_send_event():
        await asyncio.sleep(0.5)
        handler._client._dispatcher(transport, Event(*event_args))

    return asyncio.create_task(_do_send_event())


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


async def test_irc_nickname_in_use(handler, transport):
    _send_event(
        handler, transport, "nicknameinuse", "server", "user", ["username", "nickname in use"]
    )
    with pytest.raises(HandlerError):
        await handler.setup()


@pytest.mark.parametrize("error_type", ["error", "disconnect"])
async def test_irc_error_not_connected(handler, transport, error_type):
    _send_event(handler, transport, error_type, "server", "user", ["dummy error"])
    with pytest.raises(asyncio.exceptions.CancelledError) as error_handler:
        await handler.setup()
    assert str(error_handler.value) == "dummy error"


@pytest.mark.parametrize("error_type", ["error", "disconnect"])
async def test_irc_error_while_connected(handler, transport, error_type):
    _send_event(handler, transport, "900", "server", "user")
    await handler.setup()
    _send_event(handler, transport, error_type, "server", "user", ["dummy error"])
    await handler.closed


async def test_irc_disconnect_expected(handler, transport):
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


async def test_irc_error_no_arg(handler, transport):
    setup_future = asyncio.create_task(handler.setup())
    await asyncio.sleep(0.5)
    handler._client._dispatcher(transport, Event("error", "server", "dummy target", []))
    with pytest.raises(asyncio.exceptions.CancelledError) as error_handler:
        await setup_future
    if sys.version_info >= (3, 11):
        # Before 3.11, a new CancelledError is raised by the task
        # https://bugs.python.org/issue45390
        assert str(error_handler.value) == "dummy target"
    transport.write.assert_called_with(b"QUIT :Connection cancelled\r\n")
    transport.close.assert_called_with()


@pytest.mark.timeout(10)
async def test_irc_no_loggedin(handler, transport):
    setup_future = asyncio.create_task(handler.setup())
    await asyncio.sleep(0.5)
    handler._client._dispatcher(
        transport,
        Event(
            "privnotice",
            "NickServ!NickServ@services.libera.chat",
            "dummy-username",
            ["You are now identified for dummy-username"],
        ),
    )
    await setup_future


async def test_irc_privnotice_and_loggedin(handler, transport):
    setup_future = asyncio.create_task(handler.setup())
    await asyncio.sleep(0.5)
    handler._client._dispatcher(
        transport,
        Event(
            "privnotice",
            "NickServ!NickServ@services.libera.chat",
            "dummy-username",
            ["You are now identified for dummy-username"],
        ),
    )
    await asyncio.sleep(0.5)
    handler._client._dispatcher(
        transport,
        Event(
            "loggedin",
            "server",
            "dummy-username",
        ),
    )
    await setup_future


@pytest.mark.parametrize(
    "source,args",
    [
        ("wrong-source", ["You are now identified for dummy-username"]),
        ("NickServ!NickServ@services.libera.chat", ["wrong-message"]),
        ("NickServ!NickServ@services.libera.chat", []),
        ("wrong-source", ["wrong-message"]),
    ],
)
def test_irc_unrelated_privnotice(handler, transport, source, args):
    handler._client._loop = Mock()
    handler._client._dispatcher(
        transport,
        Event(
            "privnotice",
            source,
            "dummy-username",
            args,
        ),
    )
    handler._client._loop.call_later.assert_not_called()
