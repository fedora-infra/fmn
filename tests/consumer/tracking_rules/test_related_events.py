import pytest

from fmn.consumer.tracking_rule import RelatedEvents

from ..conftest import Message


@pytest.mark.parametrize(
    "received,expected",
    [(["user1", "user2"], True), (["user2"], False)],
)
def test_related_events(requester, received, expected):
    tr = RelatedEvents(requester, {"username": "user1"})
    msg = Message(topic="dummy", body={"usernames": received})
    assert tr.matches(msg) is expected


def test_users_followed_cache(requester):
    tr = RelatedEvents(requester, {"username": "user1"})
    cache = {"usernames": set()}
    tr.prime_cache(cache)
    assert cache["usernames"] == set(["user1"])
