import pytest

from fmn.cache import configure_cache


@pytest.fixture(autouse=True)
async def configured_cache():
    configure_cache()
