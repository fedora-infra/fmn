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


@pytest.mark.parametrize("with_arg", ("with-arg", "without-arg"))
@pytest.mark.parametrize("with_self", ("with-self", "without-self"))
def test_get_pattern_for_cached_calls(with_self, with_arg):
    class TestClass:
        def __str__(self):
            return "TestClass()"

        if with_arg == "with-arg":

            @cache(ttl="1h")
            def test_method(self, arg):
                return "this is test_method"

        else:

            @cache(ttl="1h")
            def test_method(self):
                return "this is test_method"

    test_object = TestClass()

    if with_self == "with-self":
        kwargs = {"self": test_object}
        expected_self = "TestClass()"
    else:
        kwargs = {}
        expected_self = "*"

    patterns = util.get_pattern_for_cached_calls(test_object.test_method, **kwargs)

    assert any(
        f":self:{expected_self}:" in pattern
        if with_arg == "with-arg"
        else pattern.endswith(f":self:{expected_self}")
        for pattern in patterns
    )
