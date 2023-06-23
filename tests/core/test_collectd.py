# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
import sys
from datetime import datetime, timezone
from unittest.mock import AsyncMock, Mock

import pytest

from fmn.database.model import Rule, User


@pytest.fixture
def collectd(monkeypatch):
    mod = Mock(name="collectd-api")
    with monkeypatch.context() as mp:
        mp.setitem(sys.modules, "collectd", mod)
        from fmn.core import collectd

    return collectd


@pytest.fixture
def created_values(collectd):
    """Record created Values instances"""
    values = []

    def _create_values():
        v = Mock()
        values.append(v)
        return v

    collectd.collectd.Values = _create_values
    return values


@pytest.fixture
def scan_result(collectd, monkeypatch):
    cache = Mock()
    monkeypatch.setattr(collectd, "cache", cache)
    scan_result = AsyncMock()
    cache.scan.return_value = scan_result
    results = []
    scan_result.__aiter__.return_value = results
    return results


@pytest.fixture
def collector(collectd):
    collector = collectd.Collector({"Interval": 60})
    collector._loop = asyncio.get_event_loop()
    return collector


def test_registration(collectd):
    collectd.collectd.register_config.assert_called_once()


class ConfigItem:
    def __init__(self, key=None, values=None):
        self.parent = None
        self.children = []
        self.key = key
        self.values = values or []
        if not hasattr(self.values, "__iter__"):
            self.values = [self.values]

    def add_child(self, item):
        item.parent = self
        self.children.append(item)


def test_configure(collectd, monkeypatch):
    collector = Mock()
    Collector = Mock(return_value=collector)
    monkeypatch.setattr("fmn.core.collectd.Collector", Collector)
    config = ConfigItem()
    config.add_child(ConfigItem(key="SetEnv", values=("foo", "bar")))
    config.add_child(ConfigItem(key="Interval", values=42))
    collectd.configure(config)
    Collector.assert_called_once_with(config={"Interval": 42, "Hostname": None})
    collectd.collectd.register_init.assert_called_once_with(collector.setup)
    collectd.collectd.register_shutdown.assert_called_once_with(collector.shutdown)
    collectd.collectd.register_read.assert_called_once_with(collector.collect, 42)


def test_configure_invalid(collectd, monkeypatch):
    config = ConfigItem()
    config.add_child(ConfigItem(key="foobar", values=("multiple", "values")))
    Collector = Mock()
    monkeypatch.setattr("fmn.core.collectd.Collector", Collector)

    collectd.configure(config)
    collectd.collectd.warning.assert_called_once_with(
        "Invalid configuration value for foobar: ('multiple', 'values')"
    )
    Collector.assert_called_once_with(config={"Interval": "60", "Hostname": None})


def test_collector_setup_shutdown(collectd, monkeypatch):
    configure_cache = Mock()
    monkeypatch.setattr(collectd, "configure_cache", configure_cache)
    db_manager = Mock()
    monkeypatch.setattr(collectd, "get_manager", Mock(return_value=db_manager))
    set_event_loop = Mock()
    monkeypatch.setattr(collectd.asyncio, "set_event_loop", set_event_loop)

    collector = collectd.Collector({})
    collector.setup()
    configure_cache.assert_called_once_with(db_manager=db_manager)
    set_event_loop.assert_called_once_with(collector._loop)
    set_event_loop.reset_mock()

    assert collector._loop.is_closed() is False

    async def do_nothing():
        await asyncio.sleep(120)

    # Create a task to make sure it gets cancelled on shutdown
    task = collector._loop.create_task(do_nothing())

    collector.shutdown()
    assert collector._loop.is_closed()
    set_event_loop.assert_called_once_with(None)
    assert task.cancelled


def test_collect_sync(collectd, monkeypatch):
    set_event_loop = Mock()
    monkeypatch.setattr(collectd.asyncio, "set_event_loop", set_event_loop)
    collector = collectd.Collector({})
    collector._collect = AsyncMock()
    collector.setup()
    collector.collect()
    collector._collect.assert_awaited_once_with()
    collector._loop.close()


async def test_collect(
    collectd, monkeypatch, collector, created_values, db_manager, db_model_initialized, scan_result
):
    # Setup dummy cache data
    dt1 = datetime(2023, 1, 1, 1, 0, 0, tzinfo=timezone.utc)
    dt2 = datetime(2023, 1, 1, 1, 30, 0, tzinfo=timezone.utc)
    dt3 = datetime(2022, 12, 31, 0, 0, 0, tzinfo=timezone.utc)
    scan_result.extend(
        [
            f"duration:statname:{dt1.isoformat()}",
            f"duration:statname:{dt2.isoformat()}",
            f"duration:statname:{dt3.isoformat()}",
        ]
    )
    collectd.cache.get = AsyncMock(side_effect=lambda key: 42)
    # Setup dummy DB data
    rule = Rule(id=1, name="dummy", user=User(name="dummy"), generation_rules=[])
    async with db_manager.Session.begin() as session:
        session.add(rule)
    # Mock now()
    mocked_dt = Mock()
    mocked_dt.now = Mock(return_value=datetime(2023, 1, 1, 1, 0, 0, tzinfo=timezone.utc))
    mocked_dt.fromisoformat = datetime.fromisoformat
    monkeypatch.setattr(collectd, "datetime", mocked_dt)

    collector.db_manager = db_manager
    await collector._collect()

    # 1 cache rebuild value, 1 active_users value
    assert len(created_values) == 2
    assert all(v.interval == 60 for v in created_values)
    assert created_values[0].type == "fmn_cache"
    assert created_values[0].plugin == "cache"
    assert created_values[0].type_instance == "statname"
    created_values[0].dispatch.assert_called_once_with(values=[42])
    assert created_values[1].type == "fmn_users"
    assert created_values[1].plugin == "users"
    assert created_values[1].type_instance == "active_users"
    created_values[1].dispatch.assert_called_once_with(values=[1])


async def test_collect_none(collectd, collector, created_values, scan_result, db_model_initialized):
    scan_result.extend(
        [
            f"duration:statname:{datetime.now().isoformat()}",
        ]
    )
    collectd.cache.get = AsyncMock(side_effect=lambda key: None)

    await collector._collect_cache()
    assert len(created_values) == 0


async def test_collect_no_data(collector, created_values, scan_result, db_model_initialized):
    await collector._collect_cache()
    assert len(created_values) == 0


async def test_collect_with_hostname(
    collectd, created_values, scan_result, db_manager, db_model_initialized
):
    scan_result.extend(
        [
            f"duration:statname:{datetime.now().isoformat()}",
        ]
    )
    collectd.cache.get = AsyncMock(side_effect=lambda key: 42)

    collector = collectd.Collector({"Interval": 60, "Hostname": "dummyhost.example.com"})
    collector._loop = asyncio.get_event_loop()
    collector.db_manager = db_manager
    await collector._collect()

    assert len(created_values) == 2
    assert all(v.host == "dummyhost.example.com" for v in created_values)


def test_dispatch_with_subname(collector, created_values):
    collector._dispatch(
        42,
        "statname",
        data_type="stattype",
        timestamp=datetime.now().timestamp(),
        subname="statsubname",
        category="category",
    )
    assert len(created_values) == 1
    assert created_values[0].type_instance == "statname-statsubname"


def test_dispatch_with_multiple_values(collector, created_values):
    collector._dispatch([42, 43], "statname", data_type="stattype")
    assert len(created_values) == 1
    created_values[0].dispatch.assert_called_once_with(values=[42, 43])
