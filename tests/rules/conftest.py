import pytest
from cashews import cache

from fmn.cache import configure_cache


@pytest.fixture(autouse=True)
async def configured_cache():
    configure_cache()
    yield
    await cache.clear()
    await cache.close()
    cache._get_backend_and_config.cache_clear()
