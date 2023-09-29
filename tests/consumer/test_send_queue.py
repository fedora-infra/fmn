# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
from unittest.mock import AsyncMock

import pytest
from aio_pika.exceptions import AMQPConnectionError

from fmn.consumer.send_queue import SendQueue
from fmn.rules.notification import Notification


@pytest.fixture
def connection(mocker):
    connection = AsyncMock(name="connection")
    mocker.patch("fmn.consumer.send_queue.connect_robust", return_value=connection)
    connection._channel = AsyncMock(name="channel")
    connection.channel.return_value = connection._channel
    connection._exchange = AsyncMock(name="exchange")
    connection._channel.get_exchange.return_value = connection._exchange
    return connection


@pytest.fixture
def notif():
    return Notification.parse_obj(
        {
            "protocol": "email",
            "content": {"headers": {"To": "dummy", "Subject": "dummy"}, "body": "dummy"},
        }
    )


async def test_send_queue_connect(connection):
    sq = SendQueue({"amqp_url": "amqp://"})
    await sq.connect()
    connection.channel.assert_called_once()
    assert sq._channel is connection._channel
    connection._channel.get_exchange.assert_called_once_with("amq.direct")
    assert sq._exchange is connection._exchange


async def test_send_queue_send(connection, notif):
    sq = SendQueue({"amqp_url": "amqp://"})
    await sq.connect()
    await sq.send(notif)
    sq._exchange.publish.assert_called_once()
    assert sq._exchange.publish.call_args.kwargs.get("routing_key") == "send.email"
    sent_msg = sq._exchange.publish.call_args.args[0]
    assert (
        sent_msg.body == b'{"headers": {"To": "dummy", "Subject": "dummy"}, '
        b'"body": "dummy", "footer": null}'
    )


async def test_send_queue_close(connection):
    sq = SendQueue({"amqp_url": "amqp://"})
    await sq.connect()
    await sq.close()
    connection.close.assert_called_once()


async def test_send_queue_close_not_connected(connection):
    sq = SendQueue({"amqp_url": "amqp://"})
    await sq.close()
    connection.close.assert_not_called()


async def test_send_queue_connect_ssl(mocker):
    tls_config = {
        "ca_cert": "ca.crt",
        "certfile": "cert.pem",
        "keyfile": "key.pem",
    }
    connection_factory = mocker.patch("fmn.consumer.send_queue.connect_robust")
    sq = SendQueue(
        {
            "amqp_url": "amqp://",
            "tls": tls_config,
        }
    )
    await sq.connect()
    connection_factory.assert_called_once()
    url = connection_factory.call_args.args[0]
    assert url.query.get("connection_name") == "FMN consumer to sender"
    assert url.query.get("cafile") == "ca.crt"
    assert url.query.get("certfile") == "cert.pem"
    assert url.query.get("keyfile") == "key.pem"


async def test_send_queue_reconnect_give_up(connection, notif, caplog):
    sq = SendQueue({"amqp_url": "amqp://"})
    await sq.connect()
    error = AMQPConnectionError("dummy error")
    connection._exchange.publish.side_effect = error

    with pytest.raises(AMQPConnectionError):
        await sq.send(notif)

    assert connection._exchange.publish.call_count == 3

    logs = [r for r in caplog.records if r.name.startswith("fmn.consumer.send_queue")]
    assert len(logs) == 3
    for log in logs[:2]:
        assert log.levelno == logging.WARNING
        assert log.msg.startswith("Publishing message failed. Retrying.")
    assert logs[2].levelno == logging.ERROR
    assert logs[2].msg.startswith("Publishing message failed. Giving up.")


async def test_send_queue_reconnect_success(connection, notif, caplog):
    sq = SendQueue({"amqp_url": "amqp://"})
    await sq.connect()
    error = AMQPConnectionError("dummy error")
    connection._exchange.publish.side_effect = [error, error, None]

    await sq.send(notif)

    assert connection._exchange.publish.call_count == 3

    logs = [r for r in caplog.records if r.name.startswith("fmn.consumer.send_queue")]
    assert len(logs) == 2
