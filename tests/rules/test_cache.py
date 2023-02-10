from unittest.mock import Mock

import pytest
from cashews import cache
from cashews.formatter import get_templates_for_func

from fmn.cache.tracked import TrackedCache
from fmn.database.model import Rule, TrackingRule, User


@pytest.fixture
def requester():
    return Mock(name="requester")


@pytest.fixture
def rule():
    tr = TrackingRule(id=1, name="artifacts-owned", params={"username": "dummy"})
    return Rule(id=1, user=User(name="dummy"), tracking_rule=tr, generation_rules=[])


async def test_build_tracked(mocker, requester, db_async_session):
    tr = TrackingRule(id=1, name="artifacts-owned", params={"username": "dummy"})
    rule = Rule(id=1, name="dummy", user=User(name="dummy"), tracking_rule=tr, generation_rules=[])
    db_async_session.add_all([rule, tr])
    prime_cache = mocker.patch.object(tr, "prime_cache")
    tracked_cache = TrackedCache()
    tracked = await tracked_cache.build(db_async_session, requester)
    prime_cache.assert_called_once_with(tracked, requester)


async def test_get_tracked(mocker, requester):
    db = Mock()
    tracked_cache = TrackedCache()
    # configure_cache()
    mocker.patch.object(tracked_cache, "build", return_value="tracked_value")
    result1 = await tracked_cache.get_tracked(db, requester)
    result2 = await tracked_cache.get_tracked(db, requester)
    tracked_cache.build.assert_called_once_with(db=db, requester=requester)
    assert result1 == "tracked_value"
    assert result2 == "tracked_value"


@pytest.mark.cashews_cache(enabled=True)
async def test_invalidate_tracked(mocker, requester):
    mocker.patch.object(cache, "delete")
    tracked_cache = TrackedCache()
    await tracked_cache.invalidate()
    cache_key = list(get_templates_for_func(tracked_cache.get_tracked))[0]
    cache.delete.assert_called_with(cache_key)


@pytest.mark.parametrize(
    "topic,expected",
    [
        ("dummy.topic", False),
        ("fmn.rule.create.v1", True),
        ("fmn.rule.update.v1", True),
        ("fmn.rule.delete.v1", True),
    ],
)
async def test_invalidate_on_message(mocker, topic, expected, make_mocked_message):
    message = make_mocked_message(topic=topic, body={})
    tracked_cache = TrackedCache()
    mocker.patch.object(tracked_cache, "invalidate")
    # # Set an existing value that will be invalidated
    # existing_value = Tracked(packages={"existing"}, usernames={"existing"})
    # cache_key = list(get_templates_for_func(tracked_cache.get_tracked))[0]
    # # It's an "early" strategy so we need to store according to the interface
    # early_expire_at = datetime.utcnow() + timedelta(seconds=3600)
    # await cache.set(cache_key, [early_expire_at, existing_value], expire=86400)
    await tracked_cache.invalidate_on_message(message)
    if expected:
        tracked_cache.invalidate.assert_called_once_with()
    else:
        tracked_cache.invalidate.assert_not_called()
