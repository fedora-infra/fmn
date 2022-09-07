import json
from unittest.mock import AsyncMock, MagicMock, Mock
from uuid import uuid4

import pytest
from aio_pika.channel import Channel
from aio_pika.message import IncomingMessage
from aio_pika.queue import Queue, QueueIterator
from aiormq.abc import ContentHeader, DeliveredMessage, spec

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
    return channel


async def test_connect(mocked_connection, mocked_channel):
    handler = Mock(name="handler")
    consumer = Consumer("amqp://rmq.example.com/%2Fvhost", "testdest", handler)
    await consumer.connect()
    mocked_connection.channel.assert_called_once_with()
    mocked_channel.declare_queue.assert_called_once_with(
        "testdest", durable=True, auto_delete=False, exclusive=False
    )
    mocked_channel.mocked_queue.bind.assert_called_once_with("amq.direct", "send.testdest")


async def test_consume(mocked_channel):
    handler = MagicMock(name="handler", spec=Handler)
    consumer = Consumer("amqp://rmq.example.com/%2Fvhost", "testdest", handler)
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
    consumer._queue.iterator = Mock(return_value=iterator)

    future = consumer.start()
    await iterator.on_message(make_message(mocked_channel, {"foo": "bar"}))
    await iterator.on_message(CLOSING)
    await future
    handler.handle.assert_called_once_with({"foo": "bar"})


async def test_stop_not_connected(mocked_channel):
    handler = MagicMock(name="handler", spec=Handler)
    consumer = Consumer("amqp://rmq.example.com/%2Fvhost", "testdest", handler)
    await consumer.stop()
    handler.stop.assert_called_once_with()


async def test_stop_not_consuming(mocked_channel):
    handler = MagicMock(name="handler", spec=Handler)
    consumer = Consumer("amqp://rmq.example.com/%2Fvhost", "testdest", handler)
    consumer._connection = Mock()
    consumer._connection.close = AsyncMock()
    await consumer.stop()
    consumer._connection.close.assert_called_once_with()
    handler.stop.assert_called_once_with()


async def test_stop_consuming(mocked_channel):
    handler = MagicMock(name="handler", spec=Handler)
    consumer = Consumer("amqp://rmq.example.com/%2Fvhost", "testdest", handler)
    consumer._connection = Mock()
    consumer._connection.close = AsyncMock()
    consumer._queue_iter = MagicMock(spec=QueueIterator)
    await consumer.stop()
    consumer._queue_iter.on_message.assert_called_once_with(CLOSING)
    consumer._queue_iter.close.assert_called_once_with()
    consumer._connection.close.assert_called_once_with()
    handler.stop.assert_called_once_with()
