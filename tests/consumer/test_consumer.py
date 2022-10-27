from unittest.mock import Mock

import pytest
from fedora_messaging.config import conf as fm_config

from fmn.consumer.consumer import Consumer
from fmn.core import config
from fmn.database import model
from fmn.database.setup import setup_db_schema


@pytest.fixture
def mocked_cache(mocker):
    cache = mocker.patch("fmn.consumer.consumer.cache")
    cache.get_tracked.return_value = {
        "packages": set(),
        "containers": set(),
        "modules": set(),
        "flatpaks": set(),
        "usernames": set(),
        "agent_name": set(),
    }
    return cache


@pytest.fixture
def mocked_requester_class(mocker):
    requester = Mock(name="requester")
    return mocker.patch("fmn.consumer.consumer.Requester", return_value=requester)


@pytest.fixture
def mocked_send_queue_class(mocker):
    mocker.patch.dict(fm_config["consumer_config"], {"send_queue": "SEND_QUEUE_CONFIG"})
    send_queue = Mock(name="send_queue")
    return mocker.patch("fmn.consumer.consumer.SendQueue", return_value=send_queue)


def test_consumer_init(mocker, mocked_cache, mocked_requester_class, mocked_send_queue_class):
    Consumer()
    mocked_cache.configure.assert_called_once_with()
    mocked_requester_class.assert_called_once_with(
        {
            "fasjson_url": "https://fasjson.fedoraproject.org",
            "distgit_url": "https://src.fedoraproject.org",
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


def test_consumer_call_tracked(
    mocker, mocked_cache, mocked_requester_class, mocked_send_queue_class, make_mocked_message
):
    c = Consumer()
    mocked_cache.get_tracked.return_value = {
        "packages": {"pkg1"},
        "containers": set(),
        "modules": set(),
        "flatpaks": set(),
        "usernames": set(),
        "agent_name": set(),
    }

    setup_db_schema(engine=c.db.get_bind())
    user = model.User(name="dummy")
    record = model.Rule(user=user, name="the name")
    tr = model.TrackingRule(rule=record, name="artifacts-owned", params={"username": "dummy"})
    gr = model.GenerationRule(rule=record)
    f = model.Filter(generation_rule=gr, name="not_my_actions", params="dummy")
    d = model.Destination(generation_rule=gr, protocol="email", address="dummy@example.com")
    c.db.add_all([user, record, tr, gr, f, d])
    c.db.commit()

    c._requester.get_package_owners.return_value = "dummy"

    # Filtered out because of not_my_actions
    message = make_mocked_message(
        topic="dummy.topic", body={"packages": ["pkg1"], "agent_name": "dummy"}
    )
    c(message)
    c.send_queue.send.assert_not_called()

    # Should generate a notification
    message = make_mocked_message(
        topic="dummy.topic",
        body={"packages": ["pkg1"], "agent_name": "someone"},
    )
    c(message)

    c.send_queue.send.assert_called_once()
    n = c.send_queue.send.call_args[0][0]
    assert n.protocol == "email"
    assert n.content == {
        "body": "Body of message on dummy.topic",
        "headers": {"Subject": "Message on dummy.topic", "To": "dummy@example.com"},
    }


def test_consumer_init_settings_file(
    mocker, mocked_cache, mocked_requester_class, mocked_send_queue_class
):
    mocker.patch.dict(fm_config["consumer_config"], {"settings_file": "/some/where/fmn.cfg"})
    Consumer()
    assert config._settings_file == "/some/where/fmn.cfg"


def test_consumer_call_failure(
    mocker,
    mocked_cache,
    mocked_requester_class,
    mocked_send_queue_class,
    make_mocked_message,
):
    c = Consumer()
    c.db = Mock(name="db")
    mocked_cache.get_tracked.side_effect = ValueError
    message = make_mocked_message(topic="dummy.topic", body={})
    with pytest.raises(ValueError):
        c(message)
    c.db.rollback.assert_called_once()
    c.send_queue.send.assert_not_called()


def test_consumer_call_tracked_agent_name(
    mocker, mocked_cache, mocked_requester_class, mocked_send_queue_class, make_mocked_message
):
    c = Consumer()
    mocked_cache.get_tracked.return_value = {
        "packages": set(),
        "containers": set(),
        "modules": set(),
        "flatpaks": set(),
        "usernames": set(),
        "agent_name": {"dummy"},
    }

    message = make_mocked_message(
        topic="dummy.topic", body={"packages": ["pkg1"], "agent_name": "dummy"}
    )
    assert c.is_tracked(message) is True
    c.send_queue.send.assert_not_called()
