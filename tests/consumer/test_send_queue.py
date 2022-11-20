import ssl
from pathlib import Path
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
    sq.send(Notification(protocol="email", content={"dummy": "content"}))
    connection._channel.basic_publish.assert_called_with(
        exchange="amq.direct", routing_key="send.email", body='{"dummy": "content"}'
    )


def test_send_queue_close(connection):
    sq = SendQueue({"url": "amqp://"})
    sq.connect()
    sq.close()
    connection.close.assert_called_once()


def test_send_queue_connect_ssl(mocker, tmp_path: Path):
    tls_config = {
        "ca_cert": tmp_path.joinpath("ca.crt"),
        "certfile": tmp_path.joinpath("cert.pem"),
        "keyfile": tmp_path.joinpath("key.pem"),
    }
    for name, path in tls_config.items():
        with open(path, "w") as fh:
            fh.write(name)
    connection_factory = mocker.patch("fmn.consumer.send_queue.pika.BlockingConnection")
    mocker.patch.object(ssl.SSLContext, "load_verify_locations")
    mocker.patch.object(ssl.SSLContext, "load_cert_chain")
    sq = SendQueue(
        {
            "url": "amqp://",
            "tls": tls_config,
        }
    )
    sq.connect()
    connection_factory.assert_called_once()
    url_parameters = connection_factory.call_args_list[0][0][0]
    assert url_parameters.ssl_options is not None
    ssl_context = url_parameters.ssl_options.context
    assert ssl_context.minimum_version == ssl.TLSVersion.TLSv1_2
    assert ssl_context.check_hostname is True
    assert url_parameters.ssl_options.server_hostname == "localhost"
