import pytest

from fmn.rules.cache import cache


@pytest.fixture(autouse=True, scope="session")
def configured_cache():
    cache.configure()
