from typing import Iterator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..database import async_session_maker, model


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


async def query_rule(session, *filters):
    query = (
        select(model.Rule)
        .join(model.User)
        .options(
            selectinload(model.Rule.tracking_rule),
            selectinload(model.Rule.generation_rules),
            selectinload(model.Rule.generation_rules, model.GenerationRule.destinations),
            selectinload(model.Rule.generation_rules, model.GenerationRule.filters),
        )
        .where(*filters)
    )
    return await session.execute(query)
