# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from unittest import mock

import pytest


@pytest.fixture(autouse=True)
async def cache_db_model_initialized(db_manager, monkeypatch):
    monkeypatch.setattr("fmn.cache.base.get_manager", mock.Mock(return_value=db_manager))
