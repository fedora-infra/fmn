import json
import logging
import sys
import traceback

import backoff
import pika

from fmn.rules.notification import Notification

from .utils import configure_tls_parameters

log = logging.getLogger(__name__)


# Reconnection example:
# https://pika.readthedocs.io/en/stable/examples/blocking_consume_recover_multiple_hosts.html


def backoff_hdlr(details):
    log.warning(f"Publishing message failed. Retrying. {traceback.format_tb(sys.exc_info()[2])}")
    self = details["args"][0]
    self.connect()


def giveup_hdlr(details):
    log.error(f"Publishing message failed. Giving up. {traceback.format_tb(sys.exc_info()[2])}")


class SendQueue:
    def __init__(self, config):
        self.config = config
        self._connection = None
        self._channel = None

    def connect(self):
        parameters = pika.URLParameters(self.config["url"])
        if "tls" in self.config:
            configure_tls_parameters(parameters, self.config["tls"])
        parameters.client_properties = {"connection_name": "FMN consumer to sender"}
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()

    @backoff.on_exception(
        backoff.expo,
        pika.exceptions.AMQPConnectionError,
        max_tries=3,
        on_backoff=backoff_hdlr,
        on_giveup=giveup_hdlr,
    )
    def send(self, notification: Notification):
        body = json.dumps(notification.content)
        self._channel.basic_publish(
            exchange="amq.direct", routing_key=f"send.{notification.protocol}", body=body
        )

    def close(self):
        self._connection.close()
