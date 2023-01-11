from unittest import mock

import pytest
from cashews import cache

from fmn.cache import util
from fmn.core.config import get_settings


async def test_cache_configure(mocker):
    mocker.patch.object(cache, "setup")
    cache_settings = get_settings().cache

    util.configure_cache()

    cache.setup.assert_called_with(cache_settings.url, **cache_settings.setup_args or {})


@pytest.mark.parametrize("scope", (None, "scope", "unconfigured scope"))
def test_cashews_cache_arg(scope):
    settings = get_settings()

    expected = settings.cache.default_args.ttl

    if scope:
        settings.cache.scoped_args["scope"] = mock.Mock(ttl=5)
        if scope == "scope":
            expected = 5

    with mock.patch("fmn.cache.util.config.get_settings", return_value=settings):
        fn = util.cache_arg("ttl", scope=scope)

    assert fn() == expected
    assert fn() == expected
    assert fn() == expected

    assert fn.cache_info().misses == 1
    assert fn.cache_info().hits == 2
