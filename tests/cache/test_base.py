# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from cashews import cache

from fmn.cache import configure_cache
from fmn.core.config import get_settings


async def test_cache_configure(mocker):
    mocker.patch.object(cache, "setup")
    cache_settings = get_settings().cache

    configure_cache()

    cache.setup.assert_called_with(cache_settings.url, **cache_settings.setup_args or {})
