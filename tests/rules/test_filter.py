from unittest.mock import Mock

import pytest
from fedora_messaging import message

from fmn.rules.filter import Applications, NotMyActions, Severities, Topic


@pytest.fixture
def requester():
    return Mock(name="requester")


@pytest.mark.parametrize(
    "received,filtered,expected",
    [("app1", ["app1", "app2"], True), ("app3", ["app1", "app2"], False)],
)
def test_applications(requester, make_mocked_message, received, filtered, expected):
    msg = make_mocked_message(topic="dummy", body={"app": received})
    f = Applications(requester, filtered)
    assert f.matches(msg) is expected


@pytest.mark.parametrize(
    "received,filtered,expected",
    [
        (message.ERROR, ["warning", "error"], True),
        (message.INFO, ["warning", "error"], False),
    ],
)
def test_severities(requester, make_mocked_message, received, filtered, expected):
    msg = make_mocked_message(topic="dummy", body={}, severity=received)
    f = Severities(requester, filtered)
    assert f.matches(msg) is expected


@pytest.mark.parametrize(
    "received,filtered,expected",
    [("user1", "user1", False), ("user2", "user1", True)],
)
def test_not_my_actions(requester, make_mocked_message, received, filtered, expected):
    msg = make_mocked_message(topic="dummy", body={"agent_name": received})
    f = NotMyActions(requester, filtered)
    assert f.matches(msg) is expected


@pytest.mark.parametrize(
    "received,filtered,expected",
    [("foo.bar", "*bar*", True), ("foo.baz", "*bar*", False)],
)
def test_topic(requester, make_mocked_message, received, filtered, expected):
    msg = make_mocked_message(topic=received, body={})
    f = Topic(requester, filtered)
    assert f.matches(msg) is expected
