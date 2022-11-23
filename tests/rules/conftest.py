import pytest

from fmn.rules.cache import cache


@pytest.fixture(autouse=True)
def configured_cache():
    if not cache.region.is_configured:
        cache.configure()
    yield
    cache.region.invalidate()
