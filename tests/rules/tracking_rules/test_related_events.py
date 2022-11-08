import pytest

from fmn.rules.tracking_rules import RelatedEvents


@pytest.mark.parametrize(
    "received,expected",
    [(["user1", "user2"], True), (["user2"], False)],
)
def test_related_events(requester, make_mocked_message, received, expected):
    tr = RelatedEvents(requester, None, "user1")
    msg = make_mocked_message(topic="dummy", body={"usernames": received})
    assert tr.matches(msg) is expected


def test_users_followed_cache(requester):
    tr = RelatedEvents(requester, None, "testuser")
    cache = {"usernames": set()}
    tr.prime_cache(cache)
    assert cache["usernames"] == set(["testuser"])
