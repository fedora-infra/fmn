# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
import pathlib
from contextlib import nullcontext, suppress
from itertools import repeat
from unittest import mock

import httpx
import pytest
import respx
from cashews import cache
from click.testing import CliRunner
from fastapi import status
from fastapi.testclient import TestClient
from fedora_messaging import message
from sqlalchemy.exc import OperationalError
from sqlalchemy_helpers.fastapi import make_db_session

import fmn.api.handlers.misc
from fmn.api import main
from fmn.backends import FASJSONAsyncProxy, get_distgit_proxy, get_fasjson_proxy
from fmn.cache.tracked import Tracked, TrackedCache
from fmn.cache.util import cache_arg
from fmn.core.config import get_settings
from fmn.database.main import get_manager
from fmn.database.model import Destination, Filter, GenerationRule, Rule, TrackingRule, User

from .message import Message

TESTROOT = pathlib.Path(__file__).parent
TESTDATA = TESTROOT / "data"
FASJSON_V1_SPEC_JSON = TESTDATA / "fasjson_v1_spec.json"
JSONSCHEMA_BASE_URL = "https://json-schema.org/draft/2019-09"
JSONSCHEMA_LINKS_URL = f"{JSONSCHEMA_BASE_URL}/links"
JSONSCHEMA_LINKS_JSON = TESTDATA / "jsonschema_links.json"
JSONSCHEMA_HYPERSCHEMA_URL = f"{JSONSCHEMA_BASE_URL}/hyper-schema"
JSONSCHEMA_HYPERSCHEMA_JSON = TESTDATA / "jsonschema_hyperschema.json"


@pytest.fixture(autouse=True)
def clear_caches():
    get_settings.cache_clear()
    get_distgit_proxy.cache_clear()
    get_fasjson_proxy.cache_clear()
    fmn.api.handlers.misc.get_applications.cache_clear()


def pytest_configure(config):
    config.addinivalue_line("markers", "cashews_cache")


@pytest.fixture(autouse=True)
async def cashews_cache(monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest):
    # Use in-memory instead of shared Redis cache for testing and disable it by default.
    url = "mem://"
    enabled = False

    # request.node.iter_markers() lists markers of parent objects later, we need them early to make
    # e.g. markers on the method override those on the class.
    for node in request.node.listchain():
        for marker in node.own_markers:
            if marker.name == "cashews_cache":
                url = marker.kwargs.get("url", url)
                enabled = marker.kwargs.get("enabled", enabled)

    monkeypatch.setenv("CACHE__URL", url)
    cache.setup(url)

    if enabled:
        ctxmgr = nullcontext()
    else:
        ctxmgr = cache.disabling()

    with ctxmgr:
        yield

    with suppress(asyncio.exceptions.CancelledError):
        await cache.clear()
        await cache.close()


@pytest.fixture
async def respx_mocker():
    async with respx.mock as rxm:
        yield rxm


@pytest.fixture
def fasjson_url() -> str:
    settings = get_settings()
    return settings.services.fasjson_url


@pytest.fixture
def distgit_url() -> str:
    settings = get_settings()
    return settings.services.distgit_url


@pytest.fixture
def distgit_proxy():
    return get_distgit_proxy()


@pytest.fixture
def mocked_fasjson(fasjson_url):
    spec_v1_url = fasjson_url + "/specs/v1.json"

    with (
        FASJSON_V1_SPEC_JSON.open("r") as fasjson_v1_spec,
        JSONSCHEMA_LINKS_JSON.open("r") as jsonschema_links_spec,
        JSONSCHEMA_HYPERSCHEMA_JSON.open("r") as jsonschema_hyperschema_spec,
    ):
        fasjson_v1 = fasjson_v1_spec.read()
        jsonschema_links = jsonschema_links_spec.read()
        jsonschema_hyperschema = jsonschema_hyperschema_spec.read()

    respx.get(spec_v1_url).mock(return_value=httpx.Response(status.HTTP_200_OK, json=fasjson_v1))
    respx.get(JSONSCHEMA_LINKS_URL).mock(
        return_value=httpx.Response(status.HTTP_200_OK, json=jsonschema_links)
    )
    respx.get(JSONSCHEMA_HYPERSCHEMA_URL).mock(
        return_value=httpx.Response(status.HTTP_200_OK, json=jsonschema_hyperschema)
    )


@pytest.fixture
def mocked_fasjson_proxy(mocker, mocked_fasjson):
    """This disables authentication in the FASJSON proxy."""
    real_init = FASJSONAsyncProxy.__init__

    def unauth_init(self, *args, **kwargs):
        real_init(self, *args, **kwargs)
        self.client.auth = None

    mocker.patch.object(FASJSONAsyncProxy, "__init__", unauth_init)


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture(autouse=True)
def clear_settings(tmp_path):
    non_existing = str(tmp_path / "non-existing-file")
    # with open(non_existing, "w") as fh:
    #     fh.write("DATABASE__SQLALCHEMY__ECHO=true\n")
    with mock.patch("fmn.core.config.DEFAULT_CONFIG_FILE", new=non_existing), mock.patch(
        "fmn.core.config._settings_file", new=non_existing
    ):
        get_settings.cache_clear()
        yield


@pytest.fixture
async def db_manager(monkeypatch):
    """A fixture which creates an asynchronous database engine."""
    manager = get_manager()
    monkeypatch.setattr(
        "sqlalchemy_helpers.fastapi.manager_from_config", mock.Mock(return_value=manager)
    )
    monkeypatch.setattr("fmn.api.database.get_manager", mock.Mock(return_value=manager))
    monkeypatch.setattr("fmn.database.main.manager_from_config", mock.Mock(return_value=manager))
    yield manager
    await manager.engine.dispose()


@pytest.fixture
def client(db_manager):
    return TestClient(main.app)


@pytest.fixture
async def db_model_initialized(request, db_manager):
    """Fixture to initialize the asynchronous DB model.

    This is used so db_async_session is usable in tests.
    """
    await db_manager.create()
    yield
    try:
        await db_manager.drop()
    except OperationalError as e:
        alembic_marker = request.node.get_closest_marker("alembic_table_deleted")
        if alembic_marker is None or str(e.orig) != "no such table: alembic_version":
            raise


def make_async_iter_factory(retval, count=None):
    def _make_iter(*args, **kwargs):
        mocked_iterator = mock.MagicMock()
        mocked_iterator.__aiter__.return_value = repeat(retval, count)
        return mocked_iterator

    return _make_iter


@pytest.fixture
async def db_async_session(db_manager, db_model_initialized, monkeypatch):
    """Fixture setting up an asynchronous DB session."""
    async for session in make_db_session(db_manager):
        # Ensure path operations get the same session so that they don't rollback and close twice.
        monkeypatch.setattr("fmn.api.database.make_db_session", make_async_iter_factory(session, 1))
        yield session


@pytest.fixture
async def db_obj(request, db_async_session):
    """Fixture to create an object of a tested model type.

    This is for asynchronous test functions/methods."""
    db_obj_dependencies = request.instance._db_obj_get_dependencies()
    attrs = {**request.instance.attrs, **db_obj_dependencies}
    obj = request.instance.cls(**attrs)
    obj._db_obj_dependencies = db_obj_dependencies
    db_async_session.add(obj)
    await db_async_session.flush()

    yield obj

    await db_async_session.rollback()


# FASJSON


@pytest.fixture
def fasjson_user_data():
    user_data = {
        "username": "testuser",
        "surname": "User",
        "givenname": "Test",
        "human_name": "Test User",
        "emails": ["testuser@example.test"],
        "ircnicks": ["irc://testuser", "matrix:///testuser"],
        "locale": "en-US",
        "uri": "http://fasjson.example.test/v1/users/testuser/",
    }

    return user_data


@pytest.fixture
def fasjson_group_data():
    group_data = [
        {"groupname": name, "uri": f"http://fasjson.example.test/v1/groups/{name}/"}
        for name in ("testgroup", "fedora-contributors")
    ]

    return group_data


@pytest.fixture
def fasjson_user(respx_mocker, fasjson_user_data, fasjson_url):
    respx_mocker.get(f"{fasjson_url}/v1/users/{fasjson_user_data['username']}/").mock(
        return_value=httpx.Response(status.HTTP_200_OK, json={"result": fasjson_user_data})
    )

    return fasjson_user_data


@pytest.fixture
def fasjson_groups(respx_mocker, fasjson_user_data, fasjson_group_data, fasjson_url):
    respx_mocker.get(f"{fasjson_url}/v1/users/{fasjson_user_data['username']}/groups/").mock(
        return_value=httpx.Response(status.HTTP_200_OK, json={"result": fasjson_group_data})
    )

    return fasjson_group_data


# Database test data


@pytest.fixture
async def db_user(fasjson_user_data, db_async_session):
    user = User(name=fasjson_user_data["username"])
    db_async_session.add(user)
    await db_async_session.flush()

    yield user


@pytest.fixture
async def db_rule(db_async_session, db_user):
    tracking_rule = TrackingRule(name="artifacts-owned", params=["foo", "bar"])

    generation_rules = []
    for destination_proto_addrs in ({"email": "foo@bar"}, {"irc": "foobar", "matrix": "@foo:bar"}):
        destinations = [
            Destination(protocol=proto, address=addr)
            for proto, addr in destination_proto_addrs.items()
        ]
        generation_rules.append(
            GenerationRule(
                destinations=destinations,
                filters=[Filter(name="applications", params=["koji", "bodhi"])],
            )
        )
    rule = Rule(
        name="darule",
        user=db_user,
        tracking_rule=tracking_rule,
        generation_rules=generation_rules,
    )
    db_async_session.add(rule)
    await db_async_session.flush()

    yield rule


@pytest.fixture
async def db_rule_disabled(db_async_session):
    tracking_rule = TrackingRule(name="users-followed", params=["user1", "user2"])

    user = User(name="dudemcpants")
    db_async_session.add(user)
    await db_async_session.flush()

    destination = Destination(protocol="email", address="dude@mcpants")
    generation_rule = GenerationRule(destinations=[destination], filters=[])
    rule = Rule(
        name="disabledrule",
        user=user,
        tracking_rule=tracking_rule,
        generation_rules=[generation_rule],
        disabled=True,
    )
    db_async_session.add(rule)
    await db_async_session.flush()

    yield rule


@pytest.fixture(scope="session")
def make_mocked_message():
    message._schema_name_to_class["testmessage"] = Message
    message._class_to_schema_name[Message] = "testmessage"
    yield Message
    del message._schema_name_to_class["testmessage"]
    del message._class_to_schema_name[Message]


@pytest.fixture(scope="session")
def register_cache_arg_fns():
    cached_fns = set()

    def wrap_cache_arg(*args, **kwargs):
        fn = cache_arg(*args, **kwargs)
        cached_fns.add(fn)
        return fn

    with mock.patch("fmn.cache.util.cache_arg", wraps=wrap_cache_arg):
        yield cached_fns


@pytest.fixture(autouse=True)
def reset_cache_arg_caches(register_cache_arg_fns):
    yield

    for cached_fn in register_cache_arg_fns:
        cached_fn.cache_clear()


@pytest.fixture
def mocked_tracked_cache(mocker):
    mocked = mock.Mock()
    mocked.get_value = mock.AsyncMock(return_value=Tracked())
    mocked.invalidate_on_message = mock.AsyncMock()
    mocked.invalidate = mock.AsyncMock()
    mocked.delete = mock.AsyncMock()

    def _make_tracked_cache(*args, **kwargs):
        obj = TrackedCache(*args, **kwargs)
        obj.get_value = mocked.get_value
        obj.invalidate = mocked.invalidate
        obj.invalidate_on_message = mocked.invalidate_on_message
        obj.delete = mocked.delete
        return obj

    mocker.patch("fmn.cache.cli.TrackedCache", side_effect=_make_tracked_cache)
    mocker.patch("fmn.consumer.consumer.TrackedCache", side_effect=_make_tracked_cache)
    return mocked
