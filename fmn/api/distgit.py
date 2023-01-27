from fastapi import Depends

from ..backends import PagureAsyncProxy
from ..core.config import Settings, get_settings


def get_distgit_proxy(settings: Settings = Depends(get_settings)) -> PagureAsyncProxy:
    return PagureAsyncProxy(settings.services.distgit_url)
