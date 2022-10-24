import logging

from fasjson_client import Client as FasjsonClient
from fastapi import Depends

from ..core.config import Settings, get_settings

log = logging.getLogger(__name__)


def get_fasjson_client(settings: Settings = Depends(get_settings)):
    return FasjsonClient(settings.services.fasjson_url)
