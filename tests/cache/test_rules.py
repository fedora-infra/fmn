import pytest
from cashews import cache
from cashews.formatter import get_templates_for_func

from fmn.cache.rules import RulesCache
from fmn.database import model


async def test_no_db():
    rc = RulesCache()
    with pytest.raises(RuntimeError):
        await rc.get_rules()


@pytest.mark.cashews_cache(enabled=True)
async def test_rules_cache(mocker, db_async_session):
    rc = RulesCache()
    rc.db = db_async_session
    execute = mocker.spy(rc.db, "execute")
    user = model.User(name="dummy")
    rule = model.Rule(user=user, name="the name")
    db_async_session.add_all([user, rule])
    await db_async_session.commit()

    # First call
    rules = await rc.get_rules()
    assert len(rules) == 1
    assert rules[0] in db_async_session
    await db_async_session.commit()
    # Clear the session cache to pretend we've restarted (or we're another instance)
    db_async_session.expunge_all()
    # Call a second time
    rules = await rc.get_rules()
    assert len(rules) == 1
    execute.assert_called_once()
    assert rules[0] in db_async_session


async def test_rule_disabled(db_async_session):
    rc = RulesCache()
    rc.db = db_async_session
    user = model.User(name="dummy")
    rule = model.Rule(user=user, name="the name", disabled=True)
    db_async_session.add_all([user, rule])
    await db_async_session.commit()
    rules = await rc.get_rules()
    assert rules == []


@pytest.mark.cashews_cache(enabled=True)
async def test_invalidate(mocker):
    mocker.patch.object(cache, "delete")
    rc = RulesCache()
    await rc.invalidate()
    cache_key = list(get_templates_for_func(rc._get_rules))[0]
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
    rc = RulesCache()
    mocker.patch.object(rc, "invalidate")
    await rc.invalidate_on_message(message)
    if expected:
        rc.invalidate.assert_called_once_with()
    else:
        rc.invalidate.assert_not_called()
