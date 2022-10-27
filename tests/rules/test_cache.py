from unittest.mock import Mock

import pytest

from fmn.database.model import Rule, TrackingRule, User
from fmn.rules.cache import Cache


@pytest.fixture
def requester():
    return Mock(name="requester")


@pytest.fixture
def rule():
    tr = TrackingRule(id=1, name="artifacts-owned", params={"username": "dummy"})
    return Rule(id=1, user=User(name="dummy"), tracking_rule=tr, generation_rules=[])


def test_cache_proxy():
    region = Mock()
    cache = Cache()
    cache.region = region
    cache.cache_on_arguments(foo="bar")
    region.cache_on_arguments.assert_called_with(foo="bar")
    cache.configure(foo="bar")
    region.configure.assert_called_with(
        backend="dogpile.cache.memory", expiration_time=300, foo="bar"
    )
    cache.invalidate_tracked()
    region.delete.assert_called_with("tracked")


def test_build_tracked(mocker, requester, db_sync_session):
    tr = TrackingRule(id=1, name="artifacts-owned", params={"username": "dummy"})
    rule = Rule(id=1, name="dummy", user=User(name="dummy"), tracking_rule=tr, generation_rules=[])
    db_sync_session.add_all([rule, tr])
    prime_cache = mocker.patch.object(tr, "prime_cache")
    cache = Cache()
    tracked = cache.build_tracked(db_sync_session, requester)
    prime_cache.assert_called_once_with(tracked, requester)


def test_get_tracked(mocker, requester):
    db = Mock()
    cache = Cache()
    cache.configure()
    mocker.patch.object(cache, "build_tracked", return_value="tracked_value")
    result1 = cache.get_tracked(db, requester)
    result2 = cache.get_tracked(db, requester)
    cache.build_tracked.assert_called_once_with(db=db, requester=requester)
    assert result1 == "tracked_value"
    assert result2 == "tracked_value"


@pytest.mark.parametrize(
    "topic,expected",
    [
        ("dummy.topic", False),
        ("fmn.rule.updated", True),
    ],
)
def test_invalidate_on_message(topic, expected, make_mocked_message):
    message = make_mocked_message(topic=topic, body={})
    cache = Cache()
    cache.region = Mock()
    cache.invalidate_on_message(message)
    if expected:
        cache.region.delete.assert_called_once_with("tracked")
    else:
        cache.region.delete.assert_not_called()
