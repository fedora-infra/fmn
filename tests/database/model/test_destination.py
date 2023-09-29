# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from unittest import mock

import httpx
import pytest

from fmn.database import model
from fmn.database.model.destination import Destination, get_extra


@pytest.fixture
async def rule_obj(db_async_session):
    user = model.User(name="allkneelbeforezod")
    tracking_rule = model.TrackingRule(name="datrackingrule")
    generation_rules = [model.GenerationRule()]
    rule = model.Rule(user=user, tracking_rule=tracking_rule, generation_rules=generation_rules)
    db_async_session.add(rule)
    await db_async_session.flush()
    yield rule
    await db_async_session.rollback()


async def test_email(make_mocked_message, db_async_session, rule_obj):
    d = Destination(
        id=1,
        protocol="email",
        address="dummy@example.com",
        generation_rule_id=rule_obj.generation_rules[0].id,
    )
    db_async_session.add(d)

    message = make_mocked_message(
        topic="dummy",
        body={
            "summary": "dummy summary",
            "content": "dummy content",
            "app": "dummy",
            "url": "https://dummy.org/dummylink",
        },
    )
    result = await d.generate(message)
    assert result == {
        "headers": {"To": "dummy@example.com", "Subject": "[dummy] dummy summary"},
        "body": "dummy content\nhttps://dummy.org/dummylink",
        "footer": "Sent by Fedora Notifications: https://notifications.fedoraproject.org/rules/1",
    }


async def test_email_with_extra(make_mocked_message, mocker, db_async_session, rule_obj):
    mocker.patch(
        "fmn.database.model.destination.get_extra", mock.AsyncMock(return_value="DUMMY EXTRA")
    )
    d = Destination(
        id=1,
        protocol="email",
        address="dummy@example.com",
        generation_rule_id=rule_obj.generation_rules[0].id,
    )
    db_async_session.add(d)
    message = make_mocked_message(
        topic="dummy",
        body={
            "summary": "dummy summary",
            "content": "dummy content",
            "app": "dummy",
            "url": "https://dummy.org/dummylink",
        },
    )

    result = await d.generate(message)

    assert result == {
        "headers": {"To": "dummy@example.com", "Subject": "[dummy] dummy summary"},
        "body": "dummy content\nhttps://dummy.org/dummylink\nDUMMY EXTRA",
        "footer": "Sent by Fedora Notifications: https://notifications.fedoraproject.org/rules/1",
    }


async def test_irc(make_mocked_message):
    d = Destination(id=1, protocol="irc", address="dummy")
    message = make_mocked_message(
        topic="dummy",
        body={"summary": "dummy summary", "app": "dummy", "url": "https://dummy.org/dummylink"},
    )
    result = await d.generate(message)
    assert result == {
        "to": "dummy",
        "message": "[dummy] dummy summary https://dummy.org/dummylink",
    }


async def test_matrix(make_mocked_message):
    d = Destination(id=1, protocol="matrix", address="@dummy:example.com")
    message = make_mocked_message(
        topic="dummy",
        body={"summary": "dummy summary", "app": "dummy", "url": "https://dummy.org/dummylink"},
    )
    result = await d.generate(message)
    assert result == {
        "to": "@dummy:example.com",
        "message": "[dummy] dummy summary https://dummy.org/dummylink",
    }


async def test_unknown_protocol(make_mocked_message):
    d = Destination(id=1, protocol="unknown", address="dummy")
    message = make_mocked_message(topic="dummy", body={"summary": "dummy summary"})
    with pytest.raises(ValueError):
        await d.generate(message)


@pytest.mark.parametrize(
    "attr_name,value,expected",
    [("patch_url", "http://example.com/patch.patch", "DUMMY EXTRA"), ("patch_url", None, "")],
)
async def test_get_extra(make_mocked_message, respx_mocker, attr_name, value, expected):
    message = make_mocked_message(topic="dummy.topic", body={"summary": "dummy summary"})
    setattr(message, attr_name, value)
    if value is not None:
        respx_mocker.get(value).mock(side_effect=httpx.Response(200, text=expected))

    result = await get_extra(message)
    assert result == (f"\n{expected}\n" if expected else "")


async def test_get_extra_request_failure(make_mocked_message, respx_mocker):
    message = make_mocked_message(topic="dummy.topic", body={"summary": "dummy summary"})
    message.patch_url = "http://example.com/patch.patch"
    respx_mocker.get("http://example.com/patch.patch").mock(side_effect=httpx.Response(500))

    result = await get_extra(message)
    assert result == ""
