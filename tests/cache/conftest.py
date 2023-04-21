# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import pytest


@pytest.fixture(autouse=True)
async def cache_db_model_initialized(db_async_engine, db_async_schema, mocker):
    mocker.patch("fmn.cache.base.get_async_engine", return_value=db_async_engine)
