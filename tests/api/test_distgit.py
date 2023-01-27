from fmn.api.distgit import get_distgit_proxy
from fmn.backends import PagureAsyncProxy
from fmn.core.config import get_settings


def test_get_distgit_proxy():
    settings = get_settings()
    distgit_proxy = get_distgit_proxy(settings=settings)
    assert isinstance(distgit_proxy, PagureAsyncProxy)
    assert distgit_proxy.base_url == settings.services.distgit_url
