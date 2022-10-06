from typing import Iterator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..database import async_session_maker, model


async def gen_db_session() -> Iterator[AsyncSession]:
    """Generate database sessions for FastAPI request handlers.

    This lets users declare the session as a dependency in request handler
    functions, e.g.:

        @app.get("/path")
        def process_path(db_session: AsyncSession = Depends(gen_db_session)):
            query = select(Model).filter_by(...)
            result = await db_session.execute(query)
            ...

    :return: A :class:`sqlalchemy.ext.asyncio.AsyncSession` object for the
        current request
    """
    db_session = async_session_maker()
    try:
        yield db_session
        await db_session.commit()
    except Exception:
        await db_session.rollback()
        raise
    finally:
        await db_session.close()


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
