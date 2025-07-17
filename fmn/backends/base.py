# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
import sys
import traceback
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Callable
from copy import deepcopy
from functools import cached_property as ft_cached_property
from functools import wraps
from typing import Any

import backoff
from httpx import AsyncClient, HTTPError, HTTPStatusError

from ..core.config import get_settings

log = logging.getLogger(__name__)


def handle_http_error(default_factory):
    def backoff_hdlr(details):
        log.warning(
            "Request failed (try %s). Retrying in %ss. %s. %s",
            details["tries"],
            "{:0.1f}".format(details["wait"]),
            sys.exc_info()[1],
            traceback.format_tb(sys.exc_info()[2]),
        )

    def giveup_hdlr(details):
        log.warning(
            "Request failed after %s tries. Giving up. %s. %s",
            details["tries"],
            sys.exc_info()[1],
            traceback.format_tb(sys.exc_info()[2]),
        )

    def is_fatal(e):
        return isinstance(e, HTTPStatusError) and e.response.status_code < 500

    settings = get_settings()

    def exception_handler(f):
        @wraps(f)
        async def wrapper(*args, **kw):
            @backoff.on_exception(
                backoff.expo,
                HTTPError,
                max_tries=settings.cache.backoff_max_tries,
                giveup=is_fatal,
                on_backoff=backoff_hdlr,
                on_giveup=giveup_hdlr,
                logger=None,
            )
            async def _retrying_wrapper(*args, **kw):
                return await f(*args, **kw)

            try:
                return await _retrying_wrapper(*args, **kw)
            except HTTPError:
                log.exception("HTTP Error! args: %r, kwargs: %r", args, kw)
                return default_factory()

        return wrapper

    return exception_handler


NextPageParams = tuple[str, dict] | tuple[None, None]


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

    async def start(self):  # noqa: B027
        pass

    async def stop(self):  # noqa: B027
        pass

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

    def _get_payload_field(self, payload_field: str | None = None) -> Any:
        if payload_field is None:
            payload_field = getattr(self, "payload_field", None)
        return payload_field

    def extract_payload(self, result: dict, payload_field: str | None = None) -> Any:
        payload_field = self._get_payload_field(payload_field)
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
        response = await self.client.get(url, follow_redirects=True, **kwargs)
        response.raise_for_status()
        return response.json()

    async def get_payload(self, url: str, *, payload_field: str | None = None, **kwargs) -> Any:
        return self.extract_payload(await self.get(url, **kwargs), payload_field=payload_field)

    async def get_paginated(
        self,
        url: str,
        *,
        params: dict | None = None,
        payload_field: str | None = None,
        default_factory: Callable[[], list] = list,
        **kwargs,
    ) -> AsyncIterator:
        """Query the API and iterate over paginated results if applicable."""
        if params is None:
            params = {}
        else:
            # determine_next_page_params may modify this, ensure original object stays untouched
            params = deepcopy(params)

        payload_field = self._get_payload_field(payload_field)
        default_result = {payload_field: default_factory()}
        visited_urls_params = set()

        while url:
            result = await handle_http_error(lambda: default_result)(self.get)(
                url, params=params, **kwargs
            )

            visited_urls_params.add((url, repr(params)))

            for item in self.extract_payload(result, payload_field=payload_field):
                yield item

            url, params = self.determine_next_page_params(url, params, result)

            if (url, repr(params)) in visited_urls_params:
                raise PaginationRecursionError(
                    f"Paginated results seem to cause recursion: {url=!r} {params=!r}"
                )
