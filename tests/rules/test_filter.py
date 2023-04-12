# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from unittest.mock import Mock

import pytest
from fedora_messaging import message

from fmn.rules.filter import Applications, MyActions, Severities, Topic


@pytest.fixture
def requester():
    return Mock(name="requester")


@pytest.mark.parametrize(
    "received,filtered,expected",
    [
        ("app1", ["app1", "app2"], True),
        ("app3", ["app1", "app2"], False),
        ("app1", None, True),
        ("App1", ["aPP1"], True),
    ],
)
def test_applications(requester, make_mocked_message, received, filtered, expected):
    msg = make_mocked_message(topic="dummy", body={"app": received})
    f = Applications(requester, filtered, username="testuser")
    assert f.matches(msg) is expected


@pytest.mark.parametrize(
    "received,filtered,expected",
    [
        (message.ERROR, ["warning", "error"], True),
        (message.INFO, ["warning", "error"], False),
        (message.INFO, None, True),
        (message.DEBUG, None, False),
    ],
)
def test_severities(requester, make_mocked_message, received, filtered, expected):
    msg = make_mocked_message(topic="dummy", body={}, severity=received)
    f = Severities(requester, filtered, username="testuser")
    assert f.matches(msg) is expected


@pytest.mark.parametrize(
    "received,filtered,active,expected",
    [
        ("user1", "user1", True, True),
        ("user2", "user1", True, True),
        ("user1", "user1", False, False),
        ("user2", "user1", False, True),
    ],
)
def test_my_actions(requester, make_mocked_message, received, filtered, active, expected):
    msg = make_mocked_message(topic="dummy", body={"agent_name": received})
    f = MyActions(requester, active, username=filtered)
    assert f.matches(msg) is expected


@pytest.mark.parametrize(
    "received,filtered,expected",
    [("foo.bar", "*bar*", True), ("foo.baz", "*bar*", False), ("foo", None, True)],
)
def test_topic(requester, make_mocked_message, received, filtered, expected):
    msg = make_mocked_message(topic=received, body={})
    f = Topic(requester, filtered, username="testuser")
    assert f.matches(msg) is expected
