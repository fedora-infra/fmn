# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from copy import deepcopy
from functools import cached_property as ft_cached_property
from functools import wraps
from typing import Any

from httpx import AsyncClient, HTTPStatusError

log = logging.getLogger(__name__)

NextPageParams = tuple[str, dict] | tuple[None, None]


def handle_http_error(default_factory):
    def exception_handler(f):
        @wraps(f)
        async def wrapper(*args, **kw):
            try:
                return await f(*args, **kw)
            except HTTPStatusError as e:
                log.warning("Request failed: %s", e)
                return default_factory()

        return wrapper

    return exception_handler


class PaginationRecursionError(RuntimeError):
    pass


class APIClient(ABC):
    payload_field: str | None
    """The payload field in a paginated response."""

    def __init__(self, base_url: str | None = None, **kwargs):
        self.base_url = base_url

        kwargs.setdefault("timeout", None)
        if self.api_url is not None:
            kwargs["base_url"] = self.api_url

        self.client = AsyncClient(**kwargs)

    @ft_cached_property
    def base_url_with_trailing_slash(self) -> str:
        return self.base_url.rstrip("/") + "/"

    @ft_cached_property
    def api_url(self) -> str | None:
        return self.base_url

    def __str__(self) -> str:
        # Keep the try/except, don't use hasattr(), it's much slower.
        try:
            return self._str
        except AttributeError:
            clsname = type(self).__name__
            self._str = f"{clsname}({self.base_url})"
            return self._str

    def extract_payload(self, result: dict, payload_field: str | None = None) -> Any:
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

    async def get_payload(self, url: str, *, payload_field: str | None = None, **kwargs) -> Any:
        return self.extract_payload(await self.get(url, **kwargs), payload_field=payload_field)

    async def get_paginated(
        self, url: str, *, params: dict | None = None, payload_field: str | None = None, **kwargs
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
