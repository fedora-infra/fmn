from unittest.mock import Mock

import pytest

from fmn.consumer.send_queue import SendQueue
from fmn.rules.notification import Notification


@pytest.fixture
def connection(mocker):
    connection = Mock(name="connection")
    mocker.patch("fmn.consumer.send_queue.pika.BlockingConnection", return_value=connection)
    connection._channel = Mock(name="channel")
    connection.channel.return_value = connection._channel
    return connection


def test_send_queue_connect(connection):
    sq = SendQueue({"url": "amqp://"})
    sq.connect()
    connection.channel.assert_called_once()


def test_send_queue_send(connection):
    sq = SendQueue({"url": "amqp://"})
    sq.connect()
    sq.send(Notification(protocol="email", content="dummy content"))
    connection._channel.basic_publish.assert_called_with(
        exchange="amq.direct", routing_key="send.email", body='"dummy content"'
    )


def test_send_queue_close(connection):
    sq = SendQueue({"url": "amqp://"})
    sq.connect()
    sq.close()
    connection.close.assert_called_once()
