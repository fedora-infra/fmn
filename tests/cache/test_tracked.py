from unittest.mock import Mock

import pytest
from cashews import cache
from cashews.formatter import get_templates_for_func

from fmn.cache.rules import RulesCache
from fmn.cache.tracked import TrackedCache
from fmn.database.model import Rule, TrackingRule, User


@pytest.fixture
def requester():
    return Mock(name="requester")


@pytest.fixture
def rule():
    tr = TrackingRule(id=1, name="artifacts-owned", params={"username": "dummy"})
    return Rule(id=1, user=User(name="dummy"), tracking_rule=tr, generation_rules=[])


@pytest.fixture
def rules_cache(db_async_session):
    rules_cache = RulesCache()
    rules_cache.db = db_async_session
    return rules_cache


async def test_build_tracked(mocker, requester, db_async_session, rules_cache):
    tr = TrackingRule(id=1, name="artifacts-owned", params={"username": "dummy"})
    rule = Rule(id=1, name="dummy", user=User(name="dummy"), tracking_rule=tr, generation_rules=[])
    db_async_session.add_all([rule, tr])
    prime_cache = mocker.patch.object(tr, "prime_cache")
    tracked_cache = TrackedCache(requester=requester, rules_cache=rules_cache)
    tracked = await tracked_cache.get_tracked(db=db_async_session)
    prime_cache.assert_called_once_with(tracked, requester)


@pytest.mark.cashews_cache(enabled=True)
async def test_get_tracked(mocker, requester, db_async_session):
    rules_cache = mocker.AsyncMock()
    rules_cache.get_rules.return_value = []
    tracked_cache = TrackedCache(requester=requester, rules_cache=rules_cache)
    result1 = await tracked_cache.get_tracked(db=db_async_session)
    result2 = await tracked_cache.get_tracked(db=db_async_session)
    rules_cache.get_rules.assert_called_once_with(db=db_async_session)
    assert result1 == result2


@pytest.mark.cashews_cache(enabled=True)
async def test_invalidate_tracked(mocker, requester, rules_cache):
    mocker.patch.object(cache, "delete")
    tracked_cache = TrackedCache(requester=requester, rules_cache=rules_cache)
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
async def test_invalidate_on_message(
    mocker, requester, rules_cache, topic, expected, make_mocked_message
):
    message = make_mocked_message(topic=topic, body={})
    tracked_cache = TrackedCache(requester=requester, rules_cache=rules_cache)
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
