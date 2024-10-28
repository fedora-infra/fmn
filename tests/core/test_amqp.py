# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import ssl
from datetime import datetime, timezone

import pytest
from aio_pika.connection import URL

from fmn.core.amqp import get_sent_datetime, get_url_from_config


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


FAKE_NOW = datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)


@pytest.mark.parametrize(
    "sent_at,expected",
    [
        (None, FAKE_NOW),
        ("2021-07-27T04:22:42Z", datetime(2021, 7, 27, 4, 22, 42, tzinfo=timezone.utc)),
        ("2021-07-27T04:22:42JUNK", FAKE_NOW),
    ],
)
def test_get_sent_datetime(make_mocked_message, mocker, sent_at, expected):
    message = make_mocked_message(
        topic="dummy",
        body={"summary": "dummy summary"},
    )
    message._properties.headers["sent-at"] = sent_at

    fake_datetime = mocker.patch("fmn.core.amqp.datetime")
    fake_datetime.now.return_value = FAKE_NOW
    fake_datetime.fromisoformat = datetime.fromisoformat
    assert get_sent_datetime(message) == expected
