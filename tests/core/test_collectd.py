# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
import sys
from datetime import datetime, timezone
from unittest.mock import AsyncMock, Mock

import pytest


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
        print("creating valueset", v)
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
    Collector.assert_called_once_with(config={"Interval": "3600", "Hostname": None})


def test_collector_setup_shutdown(collectd, monkeypatch):
    configure_cache = Mock()
    monkeypatch.setattr(collectd, "configure_cache", configure_cache)
    collector = collectd.Collector({})
    collector.setup()
    configure_cache.assert_called_once()
    loop = asyncio.get_event_loop()
    assert loop.is_closed() is False

    async def do_nothing():
        await asyncio.sleep(120)

    # Create a task to make sure it gets cancelled on shutdown
    task = loop.create_task(do_nothing())

    collector.shutdown()
    assert loop.is_closed()
    with pytest.raises(RuntimeError):
        assert asyncio.get_event_loop()
    assert task.cancelled


def test_collect(collectd, monkeypatch, created_values, scan_result):
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
    mocked_dt = Mock()
    mocked_dt.now = Mock(return_value=datetime(2023, 1, 1, 1, 0, 0, tzinfo=timezone.utc))
    mocked_dt.fromisoformat = datetime.fromisoformat
    monkeypatch.setattr(collectd, "datetime", mocked_dt)

    collector = collectd.Collector({"Interval": 3600})
    collector.setup()
    collector.collect()

    assert len(created_values) == 2
    assert all(v.type == "fmn_cache" for v in created_values)
    assert all(v.plugin == "cache" for v in created_values)
    assert all(v.interval == 3600 for v in created_values)
    assert all(v.type_instance == "statname" for v in created_values)
    for index, dt in enumerate((dt1, dt2)):
        assert created_values[index].time == dt.timestamp()
        created_values[index].dispatch.assert_called_once_with(values=[42])


def test_collect_none(collectd, created_values, scan_result):
    scan_result.extend(
        [
            f"duration:statname:{datetime.now().isoformat()}",
        ]
    )
    collectd.cache.get = AsyncMock(side_effect=lambda key: None)

    collector = collectd.Collector({})
    collector.setup()
    collector.collect()

    assert len(created_values) == 0


def test_collect_with_hostname(collectd, created_values, scan_result):
    scan_result.extend(
        [
            f"duration:statname:{datetime.now().isoformat()}",
        ]
    )
    collectd.cache.get = AsyncMock(side_effect=lambda key: 42)

    collector = collectd.Collector({"Interval": 3600, "Hostname": "dummyhost.example.com"})
    collector.setup()
    collector.collect()

    assert len(created_values) == 1
    assert created_values[0].host == "dummyhost.example.com"


def test_dispatch_with_subname(collectd, created_values):
    collector = collectd.Collector({"Interval": 3600})
    collector._dispatch(42, "statname", datetime.now().timestamp(), "statsubname", "category")
    assert len(created_values) == 1
    assert created_values[0].type_instance == "statname-statsubname"


def test_dispatch_with_multiple_values(collectd, created_values):
    collector = collectd.Collector({"Interval": 3600})
    collector._dispatch([42, 43], "statname")
    assert len(created_values) == 1
    created_values[0].dispatch.assert_called_once_with(values=[42, 43])
