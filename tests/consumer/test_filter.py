from unittest.mock import Mock

import pytest
from fedora_messaging import message

from fmn.consumer.filter import (
    ApplicationsFilter,
    Filter,
    NotMyActionsFilter,
    SeveritiesFilter,
    TopicFilter,
)
from fmn.database.model import Filter as FilterRecord

from .conftest import Message


@pytest.fixture
def requester():
    return Mock(name="requester")


def test_from_record(requester):
    record = FilterRecord(name="not_my_actions")
    f = Filter.from_record(record, requester)
    assert isinstance(f, NotMyActionsFilter)


@pytest.mark.parametrize(
    "received,filtered,expected",
    [("app1", ["app1", "app2"], True), ("app3", ["app1", "app2"], False)],
)
def test_applications(requester, received, filtered, expected):
    msg = Message(topic="dummy", body={"app": received})
    f = ApplicationsFilter(requester, filtered)
    assert f.matches(msg) is expected


@pytest.mark.parametrize(
    "received,filtered,expected",
    [
        (message.ERROR, ["warning", "error"], True),
        (message.INFO, ["warning", "error"], False),
    ],
)
def test_severities(requester, received, filtered, expected):
    msg = Message(topic="dummy", body={}, severity=received)
    f = SeveritiesFilter(requester, filtered)
    assert f.matches(msg) is expected


@pytest.mark.parametrize(
    "received,filtered,expected",
    [("user1", "user1", False), ("user2", "user1", True)],
)
def test_not_my_actions(requester, received, filtered, expected):
    msg = Message(topic="dummy", body={"agent_name": received})
    f = NotMyActionsFilter(requester, filtered)
    assert f.matches(msg) is expected


@pytest.mark.parametrize(
    "received,filtered,expected",
    [("foo.bar", "*bar*", True), ("foo.baz", "*bar*", False)],
)
def test_topic(requester, received, filtered, expected):
    msg = Message(topic=received, body={})
    f = TopicFilter(requester, filtered)
    assert f.matches(msg) is expected
