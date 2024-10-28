# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
import ssl

from aio_pika.abc import SSLOptions
from aio_pika.connection import URL

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
