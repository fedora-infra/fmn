import asyncio
from unittest.mock import AsyncMock, Mock, call

from irc.client import Event

from fmn.sender.irc import IRCClient, IRCHandler


async def test_irc_connect(mocker):
    transport = Mock()
    aio_factory = AsyncMock(return_value=(transport, Mock()))
    aio_factory_class = mocker.patch("fmn.sender.irc.AioFactory", return_value=aio_factory)

    handler = IRCHandler({"irc_url": "ircs://username:password@irc.example.com:6697"})

    async def _send_welcome():
        await asyncio.sleep(0.5)
        handler._client._dispatcher(transport, Event("welcome", "server", "user"))

    asyncio.create_task(_send_welcome())
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
