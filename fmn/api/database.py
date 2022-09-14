from typing import Iterator

from sqlalchemy.ext.asyncio import AsyncSession

from ..database import async_session_maker


async def req_db_async_session() -> Iterator[AsyncSession]:  # pragma: no cover todo
    db_async_session = async_session_maker()
    try:
        yield db_async_session
        await db_async_session.commit()
    except Exception:
        await db_async_session.rollback()
        raise
    finally:
        await db_async_session.close()
