from fastapi import Depends

from ..backends import FASJSONAsyncProxy
from ..core.config import Settings, get_settings


def get_fasjson_proxy(settings: Settings = Depends(get_settings)) -> FASJSONAsyncProxy:
    return FASJSONAsyncProxy(base_url=settings.services.fasjson_url)
