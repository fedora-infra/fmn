# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio

import pytest

from fmn.cache.rules import RulesCache
from fmn.database import model


@pytest.mark.cashews_cache(enabled=True)
async def test_rules_cache(mocker, db_async_session):
    rc = RulesCache()
    user = model.User(name="dummy")
    rule = model.Rule(user=user, name="the name")
    db_async_session.add_all([user, rule])
    await db_async_session.commit()

    # First call
    rules = await rc.get_rules(db=db_async_session)
    assert len(rules) == 1
    assert rules[0] in db_async_session
    await db_async_session.commit()
    # Clear the session cache to pretend we've restarted (or we're another instance)
    db_async_session.expunge_all()
    # Call a second time
    rules = await rc.get_rules(db=db_async_session)
    assert len(rules) == 1
    assert rules[0] in db_async_session


async def test_rule_disabled(db_async_session):
    rc = RulesCache()
    user = model.User(name="dummy")
    rule = model.Rule(user=user, name="the name", disabled=True)
    db_async_session.add_all([user, rule])
    await db_async_session.commit()
    rules = await rc.get_rules(db=db_async_session)
    assert rules == []


@pytest.mark.cashews_cache(enabled=True)
async def test_invalidate(mocker):
    rc = RulesCache()
    mocker.patch.object(rc, "rebuild")
    db = object()
    await rc.invalidate(db)
    await asyncio.gather(*rc._background_tasks)
    rc.rebuild.assert_called_once_with()


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
    db = object()
    await rc.invalidate_on_message(message, db)
    if expected:
        rc.invalidate.assert_called_once_with(db)
    else:
        rc.invalidate.assert_not_called()
