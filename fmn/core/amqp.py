# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
import ssl
from datetime import datetime, timezone

from aio_pika.abc import SSLOptions
from aio_pika.connection import URL
from fedora_messaging.message import Message

log = logging.getLogger(__name__)


def get_url_from_config(config: dict):
    url = URL(config["amqp_url"])
    if "tls" in config:
        url = url.update_query(auth="EXTERNAL")
        url = url.update_query(
            SSLOptions(
                cafile=config["tls"]["ca_cert"],
                certfile=config["tls"]["certfile"],
                keyfile=config["tls"]["keyfile"],
                no_verify_ssl=ssl.CERT_REQUIRED,
            )
        )
    return url


def get_sent_datetime(message: Message) -> datetime:
    sent_at = message._headers.get("sent-at", None)
    if sent_at:
        # fromisoformat doesn't parse Z suffix (yet) see:
        # https://discuss.python.org/t/parse-z-timezone-suffix-in-datetime/2220
        try:
            return datetime.fromisoformat(sent_at.replace("Z", "+00:00"))
        except ValueError:
            log.exception("Failed to parse sent-at timestamp value")
    # Default to now
    return datetime.now(tz=timezone.utc)
