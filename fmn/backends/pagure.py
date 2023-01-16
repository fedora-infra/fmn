import logging

from httpx import URL, QueryParams

from ..core.util import make_synchronous
from .base import APIClient, NextPageParams

log = logging.getLogger(__name__)


class PagureAsyncProxy(APIClient):
    """Proxy for the FASJSON API endpoints used in FMN"""

    API_VERSION = "0"

    def __init__(self, base_url: str):
        super().__init__(f"{base_url.rstrip('/')}/api/{self.API_VERSION}")

    def determine_next_page_params(self, url: str, params: dict, result: dict) -> NextPageParams:
        next_url = result.get("pagination", {}).get("next")
        if next_url:
            parsed_url = URL(next_url)
            parsed_query_params = QueryParams(parsed_url.query)
            next_params = {**params, **parsed_query_params}
            next_url = str(parsed_url.copy_with(query=None))

            return next_url, next_params

        return None, None


PagureSyncProxy = make_synchronous(PagureAsyncProxy, name="PagureSyncProxy")
