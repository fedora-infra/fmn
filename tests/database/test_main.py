from contextlib import nullcontext
from unittest import mock

import pytest
from sqlalchemy.exc import NoResultFound

from fmn.core.config import get_settings
from fmn.database import main, model


class TestCustomBase:
    @pytest.mark.parametrize("obj_exists", (True, False))
    async def test_async_get(self, obj_exists, db_async_session):
        if obj_exists:
            user = model.User(name="username")
            db_async_session.add(user)
            await db_async_session.flush()
            expectation = nullcontext()
        else:
            expectation = pytest.raises(NoResultFound)

        with expectation:
            result = await model.User.async_get(db_async_session, name="username")

        if obj_exists:
            assert user.id == result.id

    @pytest.mark.parametrize("obj_exists", (True, False))
    async def test_async_get_or_create(self, obj_exists, db_async_session):
        if obj_exists:
            user = model.User(name="username")
            db_async_session.add(user)
            await db_async_session.flush()

        result = await model.User.async_get_or_create(db_async_session, name="username")

        if obj_exists:
            assert result is user

        assert result._obj_created != obj_exists


@pytest.mark.parametrize("default_engine", (True, False))
@mock.patch("fmn.database.main.sync_session_maker")
@mock.patch("fmn.database.main.get_sync_engine")
def test_init_sync_model(get_sync_engine, sync_session_maker, default_engine):
    sentinel = object()
    if default_engine:
        get_sync_engine.return_value = sentinel
        engine = None
    else:
        engine = sentinel

    main.init_sync_model(engine)

    if default_engine:
        get_sync_engine.assert_called_once_with()
    else:
        get_sync_engine.assert_not_called()
    sync_session_maker.configure.assert_called_once_with(bind=sentinel)


@pytest.mark.parametrize("default_engine", (True, False))
@mock.patch("fmn.database.main.async_session_maker", new_callable=mock.AsyncMock)
@mock.patch("fmn.database.main.get_async_engine")
async def test_init_async_model(get_async_engine, async_session_maker, default_engine):
    sentinel = object()
    if default_engine:
        get_async_engine.return_value = sentinel
        engine = None
    else:
        engine = sentinel
    # configure() is not an async coroutine, avoid warning
    async_session_maker.configure = mock.MagicMock()

    await main.init_async_model(engine)

    if default_engine:
        get_async_engine.assert_called_once_with()
    else:
        get_async_engine.assert_not_called()
    async_session_maker.configure.assert_called_once_with(bind=sentinel)


@mock.patch("fmn.database.main.create_engine")
def test_get_sync_engine(create_engine):
    main.get_sync_engine()
    create_engine.assert_called_once_with(
        url=get_settings().database.sqlalchemy.url,
        isolation_level="SERIALIZABLE",
        echo=False,
    )


@pytest.mark.parametrize(
    "in_url, out_url_or_exc",
    (
        ("sqlite:///fmn.db", "sqlite+aiosqlite:///fmn.db"),
        ("sqlite+foo:///fmn.db", "sqlite+aiosqlite:///fmn.db"),
        ("postgresql:///fmn", "postgresql+asyncpg:///fmn"),
        ("postgresql+pg8000:///fmn", "postgresql+asyncpg:///fmn"),
        ("unknowndb:///fmn", ValueError),
    ),
)
def test__async_from_sync_url(in_url, out_url_or_exc):
    if isinstance(out_url_or_exc, str):
        assert str(main._async_from_sync_url(in_url)) == out_url_or_exc
    else:
        with pytest.raises(out_url_or_exc):
            main._async_from_sync_url(in_url)


@mock.patch("fmn.database.main.create_async_engine")
def test_get_async_engine(create_async_engine):
    main.get_async_engine()
    sync_url = get_settings().database.sqlalchemy.url
    async_url = main._async_from_sync_url(sync_url)
    create_async_engine.assert_called_once_with(
        url=async_url,
        isolation_level="SERIALIZABLE",
        echo=False,
    )
