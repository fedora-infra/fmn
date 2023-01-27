from typing import Any, Sequence
from unittest import mock


class BaseTestAsyncProxy:
    CLS: type
    URL: str
    EXPECTED_API_URL: str | None
    WRAPPER_METHODS: Sequence[dict[str, Any]] = ()

    @property
    def expected_api_url(self):
        return getattr(self, "EXPECTED_API_URL", self.URL)

    def test___init__(self, proxy):
        # httpx.AsyncClient.base_url always ends in "/"
        assert proxy.client.base_url == self.expected_api_url.rstrip("/") + "/"

    def test_api_url(self, proxy):
        assert proxy.api_url == self.expected_api_url

    async def _test_wrapper_method(self, method, kwargs, params, expected_path, is_iterator, proxy):
        sentinel = object()
        if is_iterator:
            proxy.get_paginated = mock.MagicMock()
            proxy.get_paginated.return_value.__aiter__.return_value = [sentinel]
        else:
            proxy.get_payload = mock.AsyncMock()
            proxy.get_payload.return_value = sentinel

        passed_through_kwargs = {"params": params} if params else {}

        coro = getattr(proxy, method)(**(kwargs | params))
        if is_iterator:
            retval = [x async for x in coro]
            assert retval == [sentinel]
            proxy.get_paginated.assert_called_once_with(expected_path, **passed_through_kwargs)
        else:
            retval = await coro
            assert retval is sentinel
            proxy.get_payload.assert_called_once_with(expected_path, **passed_through_kwargs)

    async def test_wrapper_methods(self, proxy):
        for spec in self.WRAPPER_METHODS:
            await self._test_wrapper_method(proxy=proxy, **spec)
