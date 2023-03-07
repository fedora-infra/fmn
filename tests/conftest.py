import pathlib
from contextlib import nullcontext
from unittest import mock

import alembic.command
import httpx
import pytest
import respx
from cashews import cache
from click.testing import CliRunner
from fastapi import status
from fastapi.testclient import TestClient
from fedora_messaging import message

from fmn.api import main
from fmn.backends import FASJSONAsyncProxy, get_distgit_proxy, get_fasjson_proxy
from fmn.cache.util import cache_arg
from fmn.core.config import get_settings
from fmn.database.main import (
    Base,
    async_session_maker,
    get_async_engine,
    get_sync_engine,
    init_async_model,
    init_sync_model,
    sync_session_maker,
)
from fmn.database.migrations.main import alembic_migration
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


def pytest_configure(config):
    config.addinivalue_line("markers", "cashews_cache")


@pytest.fixture(autouse=True)
def cashews_cache(monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest):
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

    cache.clear()
    cache.close()


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
def client():
    return TestClient(main.app)


@pytest.fixture
def db_sync_engine():
    """A fixture which creates a synchronous database engine."""
    return get_sync_engine()


@pytest.fixture
def db_async_engine():
    """A fixture which creates an asynchronous database engine."""
    return get_async_engine()


@pytest.fixture
def db_sync_schema(db_sync_engine):
    """Fixture to install the database schema using the synchronous engine."""
    with db_sync_engine.begin():
        Base.metadata.create_all(db_sync_engine)
        alembic.command.stamp(alembic_migration.config, "head")


@pytest.fixture
async def db_async_schema(db_async_engine):
    """Fixture to install the database schema using the asynchronous engine."""
    async with db_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        script_dir = alembic.script.ScriptDirectory.from_config(alembic_migration.config)
        latest = script_dir.get_current_head()
        context = alembic.migration.MigrationContext.configure(
            # Not "conn" because it's async
            url=alembic_migration.config.get_main_option("sqlalchemy.url")
        )
        await conn.run_sync(context._version.create)
        await conn.execute(context._version.insert().values(version_num=latest))
        yield conn


@pytest.fixture
def db_sync_model_initialized(db_sync_engine, db_sync_schema):
    """Fixture to initialize the synchronous DB model.

    This is used so db_sync_session is usable in tests.
    """
    init_sync_model(sync_engine=db_sync_engine)


@pytest.fixture
async def db_async_model_initialized(db_async_engine, db_async_schema):
    """Fixture to initialize the asynchronous DB model.

    This is used so db_async_session is usable in tests.
    """
    await init_async_model(async_engine=db_async_engine)


@pytest.fixture
def db_sync_session(db_sync_model_initialized):
    """Fixture setting up a synchronous DB session."""
    db_session = sync_session_maker()
    try:
        yield db_session
    finally:
        db_session.close()


@pytest.fixture
async def db_async_session(db_async_model_initialized):
    """Fixture setting up an asynchronous DB session."""
    db_session = async_session_maker()
    try:
        yield db_session
    finally:
        await db_session.close()


@pytest.fixture
def db_sync_obj(request, db_sync_session):
    """Fixture to create an object of a tested model type.

    This is for synchronous test functions/methods."""
    with db_sync_session.begin():
        db_obj_dependencies = request.instance._db_obj_get_dependencies()
        attrs = {**request.instance.attrs, **db_obj_dependencies}
        obj = request.instance.cls(**attrs)
        obj._db_obj_dependencies = db_obj_dependencies
        db_sync_session.add(obj)
        db_sync_session.flush()

        yield obj

        db_sync_session.rollback()


@pytest.fixture
async def db_async_obj(request, db_async_session):
    """Fixture to create an object of a tested model type.

    This is for asynchronous test functions/methods."""
    async with db_async_session.begin():
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
