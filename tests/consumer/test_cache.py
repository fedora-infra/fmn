from unittest.mock import Mock

import pytest

from fmn.consumer.cache import Cache
from fmn.consumer.rule import Rule
from fmn.consumer.tracking_rule import ArtifactsOwned
from fmn.core.config import get_settings

from .conftest import Message


@pytest.fixture
def requester():
    return Mock(name="requester")


@pytest.fixture
def rule(mocker, requester):
    requester = Mock()
    tr = ArtifactsOwned(requester, params={"username": "dummy"})
    rule = Rule(id=1, username="dummy", tracking_rule=tr, generation_rules=[])
    mocker.patch.object(Rule, "collect", return_value=[rule])
    return rule


def test_cache_proxy():
    region = Mock()
    cache = Cache()
    cache.region = region
    cache.cache_on_arguments(foo="bar")
    region.cache_on_arguments.assert_called_with(foo="bar")
    cache.configure(foo="bar")
    region.configure.assert_called_with(foo="bar")
    cache.invalidate_tracked()
    region.delete.assert_called_with("tracked")


def test_build_tracked(mocker, requester, rule):
    db = Mock()
    collect = mocker.patch.object(Rule, "collect", return_value=[rule])
    prime_cache = mocker.patch.object(rule.tracking_rule, "prime_cache")
    cache = Cache()
    tracked = cache.build_tracked(db, requester)
    collect.assert_called_once_with(db, requester)
    prime_cache.assert_called_once_with(tracked)


def test_get_tracked(mocker, requester):
    db = Mock()
    cache = Cache()
    cache.configure(**get_settings().dict()["cache"])
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
def test_invalidate_on_message(topic, expected):
    message = Message(topic=topic, body={})
    cache = Cache()
    cache.region = Mock()
    cache.invalidate_on_message(message)
    if expected:
        cache.region.delete.assert_called_once_with("tracked")
    else:
        cache.region.delete.assert_not_called()
