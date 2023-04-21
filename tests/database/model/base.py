# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from sqlalchemy import select
from sqlalchemy.orm import selectinload


class ModelTestBase:
    cls = None
    attrs = {}
    no_validate_attrs = ()

    async def test_create_obj(self, db_obj):
        pass

    async def test_query_obj(self, db_obj, db_async_session):
        # The selectinload() option tells SQLAlchemy to load related objects and lazy loading breaks
        # things here. See here for details:
        #
        # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
        #
        # You can specify which relation you're interested in but because this code doesn't know
        # anything about the involved ORM class, we specify that we "want it all".
        result = await db_async_session.execute(select(self.cls).options(selectinload("*")))
        obj = result.scalar_one()
        for key, value in self.attrs.items():
            if key in self.no_validate_attrs:
                continue
            objvalue = getattr(obj, key)
            if isinstance(objvalue, (int, str)):
                assert objvalue == value
        for key, value in self._db_obj_get_dependencies().items():
            if key in self.no_validate_attrs:
                continue
            objvalue = getattr(obj, key)
            if isinstance(objvalue, (int, str)):
                assert objvalue == value

    def _db_obj_get_dependencies(self):
        """Get model test dependencies.

        Use this method to pull in other objects that need to be created
        for the tested model object to be built properly.
        """
        return {}
