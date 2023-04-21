# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import pytest


@pytest.fixture(autouse=True)
async def cache_db_model_initialized(db_engine, db_schema, mocker):
    mocker.patch("fmn.cache.base.get_engine", return_value=db_engine)
