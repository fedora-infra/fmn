# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import ssl

from aio_pika.connection import URL

from fmn.core.amqp import get_url_from_config


async def test_get_url_from_config_with_ssl(mocker):
    config = {
        "amqp_url": "amqp://rmq.example.com/%2Fvhost",
        "tls": {
            "ca_cert": "/path/to/cacert",
            "certfile": "/path/to/certfile",
            "keyfile": "/path/to/keyfile",
        },
    }
    expected = URL("amqp://rmq.example.com/%2Fvhost").with_query(
        {
            "auth": "EXTERNAL",
            "cafile": "/path/to/cacert",
            "certfile": "/path/to/certfile",
            "keyfile": "/path/to/keyfile",
            "no_verify_ssl": ssl.CERT_REQUIRED,
        }
    )
    assert get_url_from_config(config) == expected
