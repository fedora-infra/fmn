import logging
from abc import ABC, abstractmethod
from copy import deepcopy
from functools import cache as ft_cache
from typing import Any, AsyncIterator

from httpx import AsyncClient

log = logging.getLogger(__name__)

NextPageParams = tuple[str, dict] | tuple[None, None]


class PaginationRecursionError(RuntimeError):
    pass


class APIClient(ABC):
    payload_field: str | None
    """The payload field in a paginated response."""

    def __init__(self, base_url: str = None, **kwargs):
        self.base_url = base_url

        kwargs.setdefault("timeout", None)
        if base_url is not None:
            kwargs["base_url"] = base_url

        self.client = AsyncClient(**kwargs)

    @ft_cache
    def __str__(self) -> str:
        clsname = type(self).__name__
        return f"{clsname}({self.base_url!r})"

    def extract_payload(self, result: dict, payload_field: str = None) -> Any:
        if payload_field is None:
            payload_field = getattr(self, "payload_field", None)

        if payload_field is not None:
            return result[payload_field]

        return result

    @abstractmethod
    def determine_next_page_params(
        self, url: str, params: dict, result: dict
    ) -> NextPageParams:  # pragma: no cover
        """Determine parameters for next page.

        :param url:     API endpoint URL
        :param params:  Query parameters (can be modified)
        :param result:  Result dictionary of previous query
        :return:        Tuple of (new URL, new params dict) or (None, None)
                        if last page
        """
        raise NotImplementedError()

    async def get(self, url: str, **kwargs) -> Any:
        """Query the API for a single result."""
        response = await self.client.get(url, **kwargs)
        response.raise_for_status()
        return response.json()

    async def get_payload(self, url: str, *, payload_field: str = None, **kwargs) -> Any:
        return self.extract_payload(await self.get(url, **kwargs), payload_field=payload_field)

    async def get_paginated(
        self, url: str, *, params: dict = None, payload_field: str = None, **kwargs
    ) -> AsyncIterator:
        """Query the API and iterate over paginated results if applicable."""
        if params is None:
            params = {}
        else:
            # determine_next_page_params may modify this, ensure original object stays untouched
            params = deepcopy(params)

        visited_urls_params = set()

        while url:
            result = await self.get(url, params=params, **kwargs)

            visited_urls_params.add((url, repr(params)))

            for item in self.extract_payload(result, payload_field=payload_field):
                yield item

            url, params = self.determine_next_page_params(url, params, result)

            if (url, repr(params)) in visited_urls_params:
                raise PaginationRecursionError(
                    f"Paginated results seem to cause recursion: {url=!r} {params=!r}"
                )
