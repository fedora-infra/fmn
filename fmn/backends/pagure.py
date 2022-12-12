import logging

from httpx import AsyncClient

from ..core.util import make_synchronous
from .base import APIClient

log = logging.getLogger(__name__)


class PagureAsyncProxy(APIClient):
    """Proxy for the FASJSON API endpoints used in FMN"""

    API_VERSION = "0"

    def __init__(self, base_url: str):
        self.client = AsyncClient(
            base_url=f"{base_url.rstrip('/')}/api/{self.API_VERSION}", timeout=None
        )

    def determine_next_page_params(
        self, url: str, params: dict, result: dict
    ) -> tuple[str, dict] | tuple[None, None]:
        next_url = result.get("pagination", {}).get("next")
        if next_url:
            return next_url, params

        return None, None


PagureSyncProxy = make_synchronous(PagureAsyncProxy, name="PagureSyncProxy")
