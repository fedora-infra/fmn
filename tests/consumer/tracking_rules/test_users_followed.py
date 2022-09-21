import pytest

from fmn.consumer.tracking_rule import UsersFollowed

from ..conftest import Message


@pytest.mark.parametrize(
    "received,expected",
    [("user1", True), ("user2", False)],
)
def test_users_followed(requester, received, expected):
    tr = UsersFollowed(requester, {"username": ["user1"]})
    msg = Message(topic="dummy", body={"agent_name": received})
    assert tr.matches(msg) is expected


def test_users_followed_cache(requester):
    tr = UsersFollowed(requester, {"username": ["user1"]})
    cache = {"agent_name": set()}
    tr.prime_cache(cache)
    assert cache["agent_name"] == set(["user1"])
