# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import pytest

from fmn.database.model import Destination


def test_email(make_mocked_message):
    d = Destination(id=1, protocol="email", address="dummy@example.com")
    message = make_mocked_message(
        topic="dummy",
        body={
            "summary": "dummy summary",
            "content": "dummy content",
            "app": "dummy",
            "url": "https://dummy.org/dummylink",
        },
    )
    result = d.generate(message)
    assert result == {
        "headers": {"To": "dummy@example.com", "Subject": "[dummy] dummy summary"},
        "body": "dummy content\nhttps://dummy.org/dummylink",
    }


def test_irc(make_mocked_message):
    d = Destination(id=1, protocol="irc", address="dummy")
    message = make_mocked_message(
        topic="dummy",
        body={"summary": "dummy summary", "app": "dummy", "url": "https://dummy.org/dummylink"},
    )
    result = d.generate(message)
    assert result == {
        "to": "dummy",
        "message": "[dummy] dummy summary https://dummy.org/dummylink",
    }


def test_matrix(make_mocked_message):
    d = Destination(id=1, protocol="matrix", address="@dummy:example.com")
    message = make_mocked_message(
        topic="dummy",
        body={"summary": "dummy summary", "app": "dummy", "url": "https://dummy.org/dummylink"},
    )
    result = d.generate(message)
    assert result == {
        "to": "@dummy:example.com",
        "message": "[dummy] dummy summary https://dummy.org/dummylink",
    }


def test_unknown_protocol(make_mocked_message):
    d = Destination(id=1, protocol="unknown", address="dummy")
    message = make_mocked_message(topic="dummy", body={"summary": "dummy summary"})
    with pytest.raises(ValueError):
        d.generate(message)
