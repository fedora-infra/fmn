# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from unittest import mock

import pytest

from fmn.cache import util
from fmn.core.config import get_settings


@pytest.mark.parametrize("scope", (None, "pagure", "unconfigured scope"))
def test_cashews_cache_arg(scope):
    settings = get_settings()

    expected = settings.cache.default_args.ttl

    if scope:
        settings.cache.scoped_args.pagure = mock.Mock(ttl=5)
        if scope == "pagure":
            expected = 5

    with mock.patch("fmn.cache.util.config.get_settings", return_value=settings):
        fn = util.cache_arg("ttl", scope=scope)

    assert fn() == expected
    assert fn() == expected
    assert fn() == expected

    assert fn.cache_info().misses == 1
    assert fn.cache_info().hits == 2
