# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import json
import ssl
from unittest.mock import AsyncMock, MagicMock, Mock
from uuid import uuid4

import pytest
from aio_pika.channel import Channel
from aio_pika.message import IncomingMessage
from aio_pika.queue import Queue, QueueIterator
from aiormq.abc import ContentHeader, DeliveredMessage, spec
from yarl import URL

from fmn.sender.consumer import CLOSING, Consumer
from fmn.sender.handler import Handler


def make_message(channel, content):
    return IncomingMessage(
        message=DeliveredMessage(
            body=json.dumps(content).encode("utf-8"),
            channel=channel,
            delivery=spec.Basic.Deliver(delivery_tag=uuid4()),
            header=ContentHeader(),
        )
    )


@pytest.fixture
def consumer():
    handler = MagicMock(name="handler", spec=Handler)
    config = {"amqp_url": "amqp://rmq.example.com/%2Fvhost", "queue": "testdest"}
    consumer = Consumer(config, handler)
    return consumer


@pytest.fixture
def mocked_connection(mocker):
    connection = Mock(name="connection")
    mocker.patch("fmn.sender.consumer.connect_robust", AsyncMock(return_value=connection))
    return connection


@pytest.fixture
def mocked_channel(mocked_connection):
    channel = Mock(name="channel", spec=Channel)
    mocked_connection.channel = AsyncMock(return_value=channel)
    mocked_connection.mocked_channel = channel

    queue = Mock(name="queue")
    channel.declare_queue = AsyncMock(return_value=queue)
    channel.mocked_queue = queue
    queue.bind = AsyncMock()

    channel.basic_consume = AsyncMock()
    channel.basic_ack = AsyncMock()
    channel.is_closed = False
    return channel


async def test_connect(mocked_connection, mocked_channel, consumer):
    await consumer.connect()
    mocked_connection.channel.assert_called_once_with()
    mocked_channel.declare_queue.assert_called_once_with(
        "testdest", durable=True, auto_delete=False, exclusive=False
    )
    mocked_channel.mocked_queue.bind.assert_called_once_with("amq.direct", "send.testdest")


async def test_consume(mocked_channel, consumer, mocker):
    consumer._queue = Queue(
        mocked_channel,
        name="testqueue",
        durable=False,
        exclusive=False,
        auto_delete=False,
        arguments={},
    )
    # Make sure we always return the same iterator instance
    iterator = QueueIterator(consumer._queue)
    mocker.patch("aio_pika.queue.QueueIterator", Mock(return_value=iterator))

    future = consumer.start()
    await iterator.on_message(make_message(mocked_channel, {"foo": "bar"}))
    await iterator.on_message(CLOSING)
    await future
    consumer._handler.handle.assert_called_once_with({"foo": "bar"})


async def test_stop_not_connected(mocked_channel, consumer):
    await consumer.stop()
    consumer._handler.stop.assert_called_once_with()


async def test_stop_not_consuming(mocked_channel, consumer):
    consumer._connection = Mock()
    consumer._connection.close = AsyncMock()
    await consumer.stop()
    consumer._connection.close.assert_called_once_with()
    consumer._handler.stop.assert_called_once_with()


async def test_stop_consuming(mocked_channel, consumer):
    consumer._connection = Mock()
    consumer._connection.close = AsyncMock()
    consumer._queue_iter = MagicMock(spec=QueueIterator)
    await consumer.stop()
    consumer._queue_iter.on_message.assert_called_once_with(CLOSING)
    consumer._queue_iter.close.assert_called_once_with()
    consumer._connection.close.assert_called_once_with()
    consumer._handler.stop.assert_called_once_with()


async def test_with_ssl(mocker):
    connect_robust = AsyncMock()
    mocker.patch("fmn.sender.consumer.connect_robust", connect_robust)
    handler = MagicMock(name="handler", spec=Handler)
    config = {
        "amqp_url": "amqp://rmq.example.com/%2Fvhost",
        "queue": "testdest",
        "tls": {
            "ca_cert": "/path/to/cacert",
            "certfile": "/path/to/certfile",
            "keyfile": "/path/to/keyfile",
        },
    }
    consumer = Consumer(config, handler)
    await consumer.connect()
    connect_robust.assert_called_once_with(
        URL("amqp://rmq.example.com/%2Fvhost").with_query(
            {
                "auth": "EXTERNAL",
                "cafile": "/path/to/cacert",
                "certfile": "/path/to/certfile",
                "keyfile": "/path/to/keyfile",
                "no_verify_ssl": ssl.CERT_REQUIRED,
                "connection_name": "FMN sender on testdest",
            },
        )
    )
