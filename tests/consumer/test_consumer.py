# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
from unittest.mock import AsyncMock, Mock

import pytest
from aio_pika.exceptions import AMQPConnectionError
from fedora_messaging.config import conf as fm_config
from fedora_messaging.exceptions import Nack
from sqlalchemy import select

from fmn.cache.tracked import Tracked
from fmn.consumer.consumer import Consumer
from fmn.core import config
from fmn.database import model
from fmn.rules.notification import EmailNotificationContent, Notification


@pytest.fixture
def mocked_requester_class(mocker):
    requester = Mock(name="requester")
    requester.invalidate_on_message = AsyncMock()
    return mocker.patch("fmn.consumer.consumer.Requester", return_value=requester)


@pytest.fixture
def mocked_send_queue_class(mocker):
    mocker.patch.dict(fm_config["consumer_config"], {"send_queue": "SEND_QUEUE_CONFIG"})
    send_queue = Mock(name="send_queue")
    send_queue.connect = AsyncMock()
    send_queue.send = AsyncMock()
    return mocker.patch("fmn.consumer.consumer.SendQueue", return_value=send_queue)


@pytest.fixture
def mocked_session_maker(mocker):
    db = AsyncMock()
    transaction_manager = AsyncMock()
    transaction_manager.db = db
    db_manager = Mock()
    mocker.patch("fmn.consumer.consumer.get_manager", return_value=db_manager)
    db_manager.Session.begin.return_value = transaction_manager
    transaction_manager.__aenter__ = AsyncMock(name="sessionmakercontextmanager", return_value=db)
    return transaction_manager


async def test_consumer_init(
    mocker, mocked_tracked_cache, mocked_requester_class, mocked_send_queue_class
):
    configure_cache = mocker.patch("fmn.consumer.consumer.configure_cache")
    c = Consumer()
    await c._ready
    configure_cache.assert_called_once_with(db_manager=c.db_manager)
    mocked_requester_class.assert_called_once_with(config.get_settings().services)
    mocked_send_queue_class.assert_called_once_with("SEND_QUEUE_CONFIG")


def test_consumer_loop_not_running(
    mocker,
    mocked_tracked_cache,
    mocked_requester_class,
    mocked_send_queue_class,
    make_mocked_message,
):
    c = Consumer()
    message = make_mocked_message(topic="dummy.topic", body={"foo": "bar"})
    handle = mocker.patch.object(c, "_handle")
    c(message)
    handle.assert_called_once()


async def test_consumer_call_not_tracked(
    mocker,
    mocked_tracked_cache,
    mocked_requester_class,
    mocked_send_queue_class,
    make_mocked_message,
    mocked_session_maker,
):
    c = Consumer()
    await c._ready
    message = make_mocked_message(topic="dummy.topic", body={"foo": "bar"})
    await c.handle_or_rollback(message)

    mocked_tracked_cache.invalidate_on_message.assert_called_with(message, mocked_session_maker.db)
    c._requester.invalidate_on_message.assert_called_with(message, mocked_session_maker.db)
    c.send_queue.send.assert_not_called()
    mocked_session_maker.__aenter__.assert_called_once()
    mocked_session_maker.__aexit__.assert_called_once()


async def test_consumer_call_tracked(
    mocker,
    mocked_tracked_cache,
    mocked_requester_class,
    mocked_send_queue_class,
    make_mocked_message,
    db_model_initialized,
    db_async_session,
):
    c = Consumer()
    mocked_tracked_cache.get_value.return_value = Tracked(
        packages={"pkg1"},
        containers=set(),
        modules=set(),
        flatpaks=set(),
        usernames=set(),
        agent_name=set(),
    )
    await c._ready

    user = model.User(name="dummy")
    record = model.Rule(user=user, name="the name")
    tr = model.TrackingRule(rule=record, name="artifacts-owned", params=["dummy"])
    gr = model.GenerationRule(rule=record)
    f = model.Filter(generation_rule=gr, name="my_actions", params=False)
    d = model.Destination(generation_rule=gr, protocol="email", address="dummy@example.com")
    db_async_session.add_all([user, record, tr, gr, f, d])
    await db_async_session.commit()

    c._requester.distgit.get_project_users = AsyncMock(return_value=["dummy"])
    c._requester.fasjson.get_user = AsyncMock(return_value=dict())

    # Filtered out because of my_actions
    message = make_mocked_message(
        topic="dummy.topic",
        body={
            "packages": ["pkg1"],
            "agent_name": "dummy",
            "app": "dummy",
            "url": "https://dummy.org/dummylink",
        },
    )
    await c._handle(message, db_async_session)
    c.send_queue.send.assert_not_called()

    # Should generate a notification
    message = make_mocked_message(
        topic="dummy.topic",
        body={"packages": ["pkg1"], "agent_name": "someone"},
    )
    await c._handle(message, db_async_session)

    c.send_queue.send.assert_called_once()
    n = c.send_queue.send.call_args[0][0]
    assert n.protocol == "email"
    assert n.content == EmailNotificationContent(
        body="Body of message on dummy.topic\n",
        headers={"Subject": "Message on dummy.topic", "To": "dummy@example.com"},
        footer="Sent by Fedora Notifications: https://notifications.fedoraproject.org/rules/1",
    )

    result = await db_async_session.execute(select(model.Generated))
    generated = list(result.scalars())
    assert len(generated) == 1
    assert generated[0].count == 1


async def test_consumer_user_disabled(
    mocker,
    mocked_tracked_cache,
    mocked_requester_class,
    mocked_send_queue_class,
    make_mocked_message,
    db_model_initialized,
    db_async_session,
):
    c = Consumer()
    mocked_tracked_cache.get_value.return_value = Tracked(
        packages={"pkg1"},
        containers=set(),
        modules=set(),
        flatpaks=set(),
        usernames=set(),
        agent_name=set(),
    )
    await c._ready

    user = model.User(name="dummy")
    record = model.Rule(user=user, name="the name")
    tr = model.TrackingRule(rule=record, name="artifacts-owned", params=["dummy"])
    gr = model.GenerationRule(rule=record)
    f = model.Filter(generation_rule=gr, name="my_actions", params=False)
    d = model.Destination(generation_rule=gr, protocol="email", address="dummy@example.com")
    db_async_session.add_all([user, record, tr, gr, f, d])
    await db_async_session.commit()

    c._requester.distgit.get_project_users = AsyncMock(return_value=["dummy"])
    c._requester.fasjson.get_user = AsyncMock(return_value=None)

    message = make_mocked_message(
        topic="dummy.topic",
        body={"packages": ["pkg1"], "agent_name": "someone"},
    )
    await c._handle(message, db_async_session)

    c.send_queue.send.assert_not_called()
    rule = (
        await db_async_session.execute(select(model.Rule).where(model.Rule.name == "the name"))
    ).scalar_one()
    assert rule.disabled is True


async def test_consumer_init_settings_file(
    mocker, mocked_tracked_cache, mocked_requester_class, mocked_send_queue_class
):
    mocker.patch.dict(fm_config["consumer_config"], {"settings_file": "/some/where/fmn.cfg"})
    c = Consumer()
    assert config._settings_file == "/some/where/fmn.cfg"
    await c._ready


async def test_consumer_call_failure(
    mocker,
    mocked_tracked_cache,
    mocked_requester_class,
    mocked_send_queue_class,
    make_mocked_message,
    mocked_session_maker,
):
    c = Consumer()
    await c._ready
    mocked_tracked_cache.get_value.side_effect = ValueError
    message = make_mocked_message(topic="dummy.topic", body={})

    with pytest.raises(ValueError):
        await c.handle_or_rollback(message)

    c.send_queue.send.assert_not_called()

    mocked_session_maker.__aenter__.assert_called_once()
    mocked_session_maker.__aexit__.assert_called_once()


async def test_consumer_call_tracked_agent_name(
    mocker,
    mocked_tracked_cache,
    mocked_requester_class,
    mocked_send_queue_class,
    make_mocked_message,
):
    c = Consumer()
    mocked_tracked_cache.get_value.return_value = Tracked(
        packages=set(),
        containers=set(),
        modules=set(),
        flatpaks=set(),
        usernames=set(),
        agent_name={"dummy"},
    )

    message = make_mocked_message(
        topic="dummy.topic", body={"packages": ["pkg1"], "agent_name": "dummy"}
    )
    await c._ready
    assert (await c.is_tracked(message, None)) is True


async def test_consumer_deprecated_schema(
    mocker,
    mocked_tracked_cache,
    mocked_requester_class,
    mocked_send_queue_class,
    make_mocked_message,
):
    c = Consumer()
    mocked_tracked_cache.get_value.return_value = Tracked(packages={"pkg1"})
    c._rules_cache = mocker.AsyncMock()
    message = make_mocked_message(
        topic="dummy.topic",
        body={"packages": ["pkg1"]},
    )
    mocker.patch.object(message.__class__, "deprecated", True)
    await c._handle(message, Mock())
    c._rules_cache.get_rules.assert_not_called()


async def test_consumer_send_error(
    make_mocked_message,
    mocked_requester_class,
    mocked_send_queue_class,
):
    c = Consumer()
    c.send_queue.send.side_effect = AMQPConnectionError()
    message = make_mocked_message(topic="dummy.topic", body={})

    with pytest.raises(Nack):
        await c._send(
            Notification.parse_obj(
                {"protocol": "irc", "content": {"to": "dummy", "message": "foobar"}}
            ),
            message,
        )


async def test_consumer_in_threadpool(
    mocker,
    mocked_tracked_cache,
    mocked_requester_class,
    mocked_send_queue_class,
    make_mocked_message,
):
    # Fedora Messaging >= 3.3.0 runs with the asyncio reactor, but will still run the consumer in a
    # threadpool because it's __call__() method is not async. Once we do that, this test can be
    # removed.
    loop = asyncio.get_event_loop()
    c = Consumer()
    handle = mocker.patch.object(c, "_handle")
    message = make_mocked_message(topic="dummy.topic", body={"foo": "bar"})
    await loop.run_in_executor(None, c, message)
    handle.assert_called_once()


async def test_consumer_duplicate(
    mocker,
    mocked_tracked_cache,
    mocked_requester_class,
    mocked_send_queue_class,
    make_mocked_message,
    db_model_initialized,
    db_async_session,
):
    c = Consumer()
    mocked_tracked_cache.get_value.return_value = Tracked(
        packages={"pkg1"},
        containers=set(),
        modules=set(),
        flatpaks=set(),
        usernames=set(),
        agent_name=set(),
    )
    await c._ready

    # Create two identical rules
    user = model.User(name="dummy")
    db_async_session.add(user)
    for i in range(2):
        rule = model.Rule(user=user, name=f"Rule {i}")
        db_async_session.add(rule)
        rule.tracking_rule = model.TrackingRule(
            name="artifacts-followed", params=[{"name": "pkg1", "type": "rpms"}]
        )
        gr1 = model.GenerationRule()
        gr1.destinations.append(model.Destination(protocol="email", address="dummy@example.com"))
        rule.generation_rules.append(gr1)

    await db_async_session.commit()
    # Pretend the user exists
    c._requester.fasjson.get_user = AsyncMock(return_value=dict())

    # This should generate a single notification
    message = make_mocked_message(
        topic="dummy.topic",
        body={"packages": ["pkg1"], "agent_name": "someone"},
    )
    await c._handle(message, db_async_session)

    # Only one notification should have been sent
    c.send_queue.send.assert_called_once()

    # We still consider that each rule generated a notification, even if only one was sent
    result = await db_async_session.execute(select(model.Generated))
    generated = list(result.scalars())
    assert len(generated) == 2
    assert sum(g.count for g in generated) == 2
