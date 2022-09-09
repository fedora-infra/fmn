from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import URL, Engine, make_url
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ..core.config import get_settings

# use custom metadata to specify naming convention
naming_convention = {
    "ix": "%(column_0_N_label)s_index",
    "uq": "%(table_name)s_%(column_0_N_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
metadata = MetaData(naming_convention=naming_convention)
Base = declarative_base(metadata=metadata)

async_session_maker = sessionmaker(class_=AsyncSession, expire_on_commit=False, future=True)
sync_session_maker = sessionmaker(future=True, expire_on_commit=False)


def init_sync_model(sync_engine: Engine = None):
    if not sync_engine:
        sync_engine = get_sync_engine()
    sync_session_maker.configure(bind=sync_engine)


async def init_async_model(async_engine: AsyncEngine = None):
    if not async_engine:
        async_engine = get_async_engine()
    async_session_maker.configure(bind=async_engine)


def get_sync_engine():
    db_config = get_settings().dict()["database"]["sqlalchemy"]
    db_config.setdefault("isolation_level", "SERIALIZABLE")
    return create_engine(**db_config)


def _async_from_sync_url(url: URL | str) -> URL:
    """Create an async DB URL from a conventional one."""
    sync_url = make_url(url)

    try:
        dialect, _ = sync_url.drivername.split("+", 1)
    except ValueError:
        dialect = sync_url.drivername

    match dialect:
        case "sqlite":
            driver = "aiosqlite"
        case "postgresql":
            driver = "asyncpg"
        case _:
            raise ValueError(f"Don't know asyncio driver for dialect {dialect}")

    return sync_url.set(drivername=f"{dialect}+{driver}")


def get_async_engine():
    db_config = get_settings().dict()["database"]["sqlalchemy"]
    db_config.setdefault("isolation_level", "SERIALIZABLE")
    db_config["url"] = _async_from_sync_url(db_config["url"])
    return create_async_engine(**db_config)
