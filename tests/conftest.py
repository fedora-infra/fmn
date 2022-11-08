import pathlib
from unittest import mock

import pytest
import responses
from click.testing import CliRunner
from fasjson_client import Client
from fastapi.testclient import TestClient
from fedora_messaging import message

from fmn.api import main
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


@pytest.fixture
def mocked_responses():
    with responses.mock as rm:
        yield rm


@pytest.fixture
def fasjson_url() -> str:
    settings = get_settings()
    return settings.services.fasjson_url


@pytest.fixture
def mocked_fasjson(mocked_responses, fasjson_url):
    spec_v1_url = fasjson_url + "/specs/v1.json"

    with (
        FASJSON_V1_SPEC_JSON.open("r") as fasjson_v1_spec,
        JSONSCHEMA_LINKS_JSON.open("r") as jsonschema_links_spec,
        JSONSCHEMA_HYPERSCHEMA_JSON.open("r") as jsonschema_hyperschema_spec,
    ):
        responses.get(spec_v1_url, body=fasjson_v1_spec.read())
        responses.get(JSONSCHEMA_LINKS_URL, body=jsonschema_links_spec.read())
        responses.get(JSONSCHEMA_HYPERSCHEMA_URL, body=jsonschema_hyperschema_spec.read())


@pytest.fixture
def mocked_fasjson_client(mocker, mocked_fasjson):
    """This disables authentication in the FASJSON client."""
    real_init = Client.__init__

    def unauth_init(self, url, **kwargs):
        kwargs["auth"] = False
        real_init(self, url, **kwargs)

    mocker.patch.object(Client, "__init__", unauth_init)


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture(autouse=True)
def clear_settings(tmp_path):
    non_existing = str(tmp_path / "non-existing-file")
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


@pytest.fixture
async def db_async_schema(db_async_engine):
    """Fixture to install the database schema using the asynchronous engine."""
    async with db_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


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
        "ircnicks": ["irc://testuser", "matrix://testuser"],
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
def fasjson_user(mocked_responses, fasjson_user_data, fasjson_url):
    mocked_responses.get(
        f"{fasjson_url}/v1/users/{fasjson_user_data['username']}/",
        json={"result": fasjson_user_data},
    )

    return fasjson_user_data


@pytest.fixture
def fasjson_groups(mocked_responses, fasjson_user_data, fasjson_group_data, fasjson_url):
    mocked_responses.get(
        f"{fasjson_url}/v1/users/{fasjson_user_data['username']}/groups/",
        json={"result": fasjson_group_data},
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
    for destination_proto_addrs in ({"email": "foo@bar"}, {"irc": "...", "matrix": "..."}):
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


@pytest.fixture(scope="session")
def make_mocked_message():
    message._schema_name_to_class["testmessage"] = Message
    message._class_to_schema_name[Message] = "testmessage"
    yield Message
    del message._schema_name_to_class["testmessage"]
    del message._class_to_schema_name[Message]
