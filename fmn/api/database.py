# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_helpers.fastapi import AsyncDatabaseManager, make_db_session

from ..database.main import get_manager


async def gen_db_manager() -> AsyncDatabaseManager:
    return get_manager()


DBManager = Annotated[AsyncDatabaseManager, Depends(gen_db_manager)]


async def gen_db_session(
    db_manager: AsyncDatabaseManager = Depends(gen_db_manager),
) -> Iterator[AsyncSession]:
    """Generate database sessions for FastAPI request handlers.

    This lets users declare the session as a dependency in request handler
    functions, e.g.::

        @app.get("/path")
        def process_path(db_session: AsyncSession = Depends(gen_db_session)):
            query = select(Model).filter_by(...)
            result = await db_session.execute(query)
            ...

    :return: A :class:`sqlalchemy.ext.asyncio.AsyncSession` object for the
        current request
    """
    async for session in make_db_session(db_manager):
        yield session


DBSession = Annotated[AsyncSession, Depends(gen_db_session)]
