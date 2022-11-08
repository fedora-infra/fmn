import pytest

from fmn.rules.tracking_rules import UsersFollowed


@pytest.mark.parametrize(
    "received,expected",
    [("user1", True), ("user2", False)],
)
def test_users_followed(requester, make_mocked_message, received, expected):
    tr = UsersFollowed(requester, {"username": ["user1"]}, owner="testuser")
    msg = make_mocked_message(topic="dummy", body={"agent_name": received})
    assert tr.matches(msg) is expected


def test_users_followed_cache(requester):
    tr = UsersFollowed(requester, {"username": ["user1"]}, owner="testuser")
    cache = {"agent_name": set()}
    tr.prime_cache(cache)
    assert cache["agent_name"] == set(["user1"])
