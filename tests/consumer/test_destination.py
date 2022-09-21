import pytest

from fmn.consumer.destination import IRC, Destination, Email
from fmn.database.model import Destination as DestinationRecord

from .conftest import Message


def test_from_record():
    dr1 = DestinationRecord(id=1, protocol="email", address="dummy@example.com")
    dr2 = DestinationRecord(id=2, protocol="irc", address="dummy")
    d1 = Destination.from_record(dr1)
    assert isinstance(d1, Email)
    assert d1.address == "dummy@example.com"
    d2 = Destination.from_record(dr2)
    assert isinstance(d2, IRC)
    assert d2.address == "dummy"
    with pytest.raises(ValueError):
        Destination.from_record(DestinationRecord(protocol="unknown"))


def test_email():
    d = Email("dummy@example.com")
    message = Message(topic="dummy", body={"summary": "dummy summary", "content": "dummy content"})
    result = d.generate(message)
    assert result == {
        "headers": {"To": "dummy@example.com", "Subject": "dummy summary"},
        "body": "dummy content",
    }


def test_irc():
    d = IRC("dummy")
    message = Message(topic="dummy", body={"summary": "dummy summary"})
    result = d.generate(message)
    assert result == {
        "to": "dummy",
        "message": "dummy summary",
    }
