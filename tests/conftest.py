import json
import os
from unittest import mock

import pytest
import responses
from click.testing import CliRunner
from fastapi.testclient import TestClient

from fmn.api import main
from fmn.core.config import Settings, get_settings
from fmn.database.main import (
    Base,
    async_session_maker,
    get_async_engine,
    get_sync_engine,
    init_async_model,
    init_sync_model,
    sync_session_maker,
)


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture
def client():
    def get_settings_override():
        return Settings(services={"fasjson_url": "http://fasjson.example.test"})

    def get_fasjson_client_override():
        responses.add_passthru("https://json-schema.org")
        fasjson_spec_path = os.path.join(os.path.dirname(__file__), "fixtures", "fasjson-v1.json")
        with open(fasjson_spec_path) as fasjson_spec_file:
            fasjson_spec = json.load(fasjson_spec_file)
        responses.get("http://fasjson.example.test/specs/v1.json", json=fasjson_spec)
        base_url = get_settings_override().services.fasjson_url

        return main.FasjsonClient(base_url, auth=False)

    main.app.dependency_overrides[main.get_settings] = get_settings_override
    main.app.dependency_overrides[main.get_fasjson_client] = get_fasjson_client_override
    return TestClient(main.app)


@pytest.fixture(autouse=True)
def clear_settings(tmp_path):
    non_existing = str(tmp_path / "non-existing-file")
    with mock.patch("fmn.core.config.DEFAULT_CONFIG_FILE", new=non_existing), mock.patch(
        "fmn.core.config._settings_file", new=non_existing
    ):
        get_settings.cache_clear()
        yield


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
