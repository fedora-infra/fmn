import asyncio
from unittest.mock import AsyncMock, Mock

import pytest
from aio_pika.exceptions import AMQPConnectionError
from fedora_messaging.config import conf as fm_config
from fedora_messaging.exceptions import Nack

from fmn.cache.tracked import Tracked, TrackedCache
from fmn.consumer.consumer import Consumer
from fmn.core import config
from fmn.database import model
from fmn.database.setup import setup_db_schema
from fmn.rules.notification import Notification


@pytest.fixture
def mocked_cache(mocker):
    mocker.patch.object(TrackedCache, "get_tracked", return_value=Tracked())
    mocker.patch.object(TrackedCache, "invalidate_on_message")
    return TrackedCache


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


async def test_consumer_init(mocker, mocked_cache, mocked_requester_class, mocked_send_queue_class):
    configure_cache = mocker.patch("fmn.consumer.consumer.configure_cache")
    c = Consumer()
    await c._ready
    configure_cache.assert_called_once_with()
    mocked_requester_class.assert_called_once_with(
        {
            "fasjson_url": "https://fasjson.fedoraproject.org",
            "distgit_url": "https://src.fedoraproject.org",
            "datagrepper_url": "https://apps.fedoraproject.org/datagrepper/",
        }
    )
    mocked_send_queue_class.assert_called_once_with("SEND_QUEUE_CONFIG")


def test_consumer_call_not_tracked(
    mocker,
    mocked_cache,
    mocked_requester_class,
    mocked_send_queue_class,
    make_mocked_message,
):
    c = Consumer()
    message = make_mocked_message(topic="dummy.topic", body={"foo": "bar"})
    c(message)
    mocked_cache.invalidate_on_message.assert_called_with(message)
    c._requester.invalidate_on_message.assert_called_with(message)
    c.send_queue.send.assert_not_called()


async def test_consumer_call_tracked(
    mocker, mocked_cache, mocked_requester_class, mocked_send_queue_class, make_mocked_message
):
    c = Consumer()
    mocked_cache.get_tracked.return_value = Tracked(
        packages={"pkg1"},
        containers=set(),
        modules=set(),
        flatpaks=set(),
        usernames=set(),
        agent_name=set(),
    )
    await c._ready

    await c.db.run_sync(setup_db_schema)
    user = model.User(name="dummy")
    record = model.Rule(user=user, name="the name")
    tr = model.TrackingRule(rule=record, name="artifacts-owned", params=["dummy"])
    gr = model.GenerationRule(rule=record)
    f = model.Filter(generation_rule=gr, name="my_actions", params=False)
    d = model.Destination(generation_rule=gr, protocol="email", address="dummy@example.com")
    c.db.add_all([user, record, tr, gr, f, d])
    await c.db.commit()

    c._requester.distgit.get_owners = AsyncMock(return_value=["dummy"])

    # Filtered out because of my_actions
    message = make_mocked_message(
        topic="dummy.topic", body={"packages": ["pkg1"], "agent_name": "dummy"}
    )
    await c.handle(message)
    c.send_queue.send.assert_not_called()

    # Should generate a notification
    message = make_mocked_message(
        topic="dummy.topic",
        body={"packages": ["pkg1"], "agent_name": "someone"},
    )
    await c.handle(message)

    c.send_queue.send.assert_called_once()
    n = c.send_queue.send.call_args[0][0]
    assert n.protocol == "email"
    assert n.content == {
        "body": "Body of message on dummy.topic",
        "headers": {"Subject": "Message on dummy.topic", "To": "dummy@example.com"},
    }
    await c.db.close()


async def test_consumer_rule_disabled(
    mocked_cache, mocked_requester_class, mocked_send_queue_class
):
    c = Consumer()
    await c._ready
    await c.db.run_sync(setup_db_schema)
    user = model.User(name="dummy")
    rule = model.Rule(user=user, name="the name", disabled=True)
    c.db.add_all([user, rule])
    await c.db.commit()
    rules = await c._get_rules()
    assert list(rules) == []
    await c.db.close()


async def test_consumer_init_settings_file(
    mocker, mocked_cache, mocked_requester_class, mocked_send_queue_class
):
    mocker.patch.dict(fm_config["consumer_config"], {"settings_file": "/some/where/fmn.cfg"})
    c = Consumer()
    assert config._settings_file == "/some/where/fmn.cfg"
    await c._ready
    await c.db.close()


async def test_consumer_call_failure(
    mocker,
    mocked_cache,
    mocked_requester_class,
    mocked_send_queue_class,
    make_mocked_message,
):
    c = Consumer()
    await c._ready
    await c.db.close()
    c.db = Mock(name="db")
    c.db.rollback = AsyncMock()
    mocked_cache.get_tracked.side_effect = ValueError
    message = make_mocked_message(topic="dummy.topic", body={})
    with pytest.raises(ValueError):
        await c.handle_or_rollback(message)
    c.db.rollback.assert_called_once()
    c.send_queue.send.assert_not_called()


async def test_consumer_call_tracked_agent_name(
    mocker, mocked_cache, mocked_requester_class, mocked_send_queue_class, make_mocked_message
):
    c = Consumer()
    mocked_cache.get_tracked.return_value = Tracked(
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
    assert (await c.is_tracked(message)) is True


def test_consumer_deprecated_schema(
    mocker, mocked_cache, mocked_requester_class, mocked_send_queue_class, make_mocked_message
):
    c = Consumer()
    mocked_cache.get_tracked.return_value = Tracked(packages={"pkg1"})
    mocker.patch.object(c, "_get_rules", return_value=[])
    message = make_mocked_message(
        topic="dummy.topic",
        body={"packages": ["pkg1"]},
    )
    message.__class__.deprecated = True
    c(message)
    c._get_rules.assert_not_called()


async def test_consumer_send_error(
    make_mocked_message,
    mocked_requester_class,
    mocked_send_queue_class,
):
    c = Consumer()
    c.send_queue.send.side_effect = AMQPConnectionError()
    message = make_mocked_message(topic="dummy.topic", body={})

    with pytest.raises(Nack):
        await c._send(Notification(protocol="email", content={}), message)


async def test_consumer_in_threadpool(
    mocker,
    mocked_cache,
    mocked_requester_class,
    mocked_send_queue_class,
    make_mocked_message,
):
    # Fedora Messaging >= 3.3.0 runs with the asyncio reactor, but will still run the consumer in a
    # threadpool because it's __call__() method is not async. Once we do that, this test can be
    # removed.
    loop = asyncio.get_event_loop()
    c = Consumer()
    handle = mocker.patch.object(c, "handle")
    message = make_mocked_message(topic="dummy.topic", body={"foo": "bar"})
    await loop.run_in_executor(None, c, message)
    handle.assert_called_once_with(message)
