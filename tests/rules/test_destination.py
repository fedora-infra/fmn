import pytest

from fmn.database.model import Destination


def test_email(make_mocked_message):
    d = Destination(id=1, protocol="email", address="dummy@example.com")
    message = make_mocked_message(
        topic="dummy", body={"summary": "dummy summary", "content": "dummy content"}
    )
    result = d.generate(message)
    assert result == {
        "headers": {"To": "dummy@example.com", "Subject": "dummy summary"},
        "body": "dummy content",
    }


def test_irc(make_mocked_message):
    d = Destination(id=1, protocol="irc", address="dummy")
    message = make_mocked_message(topic="dummy", body={"summary": "dummy summary"})
    result = d.generate(message)
    assert result == {
        "to": "dummy",
        "message": "dummy summary",
    }


def test_unknown_protocol(make_mocked_message):
    d = Destination(id=1, protocol="unknown", address="dummy")
    message = make_mocked_message(topic="dummy", body={"summary": "dummy summary"})
    with pytest.raises(ValueError):
        d.generate(message)
