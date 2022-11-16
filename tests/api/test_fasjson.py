from contextlib import nullcontext
from unittest import mock

import pytest

from fmn.api import fasjson


@pytest.fixture
def proxy(fasjson_url):
    proxy = fasjson.FASJSONAsyncProxy(fasjson_url)
    proxy.client = mock.AsyncMock()
    return proxy


class TestFASJSONAsyncProxy:
    PAGINATE_TOTAL_PAGES = 5
    PAGINATE_PER_PAGE = 5

    def test___init__(self):
        fasjson_url = "http://fasjson.test"
        proxy = fasjson.FASJSONAsyncProxy(fasjson_url)
        API_VERSION = fasjson.FASJSONAsyncProxy.API_VERSION
        assert proxy.client.base_url == f"{fasjson_url}/{API_VERSION.strip('/')}/"

    @classmethod
    def get_paginated_results(cls, broken=False):
        per_page = cls.PAGINATE_PER_PAGE
        total_pages = cls.PAGINATE_TOTAL_PAGES
        pages = [
            {
                "result": [{"boop": i + pageidx * per_page} for i in range(per_page)],
                "page": {"page_number": pageidx + 1, "total_pages": total_pages},
            }
            for pageidx in range(total_pages)
        ]
        if broken:
            pages[-1] = {"result": {"this is": "broken"}}
        return pages

    @classmethod
    def get_paginated_responses(cls, broken=False):
        responses = []

        for result in cls.get_paginated_results(broken=broken):
            response = mock.Mock()
            response.json.return_value = result
            responses.append(response)

        return responses

    async def test_get(self, proxy):
        proxy.client.get.return_value = response = mock.Mock()
        response.json.return_value = sentinel = object()

        result = await proxy.get("url", foo="bar")

        proxy.client.get.assert_awaited_once_with("url", foo="bar")
        response.raise_for_status.assert_called_once_with()
        assert result is sentinel

    @mock.patch("fmn.api.fasjson.FASJSONAsyncProxy.get")
    async def test_get_result(self, proxy_get, proxy):
        sentinel = object()
        proxy_get.return_value = {"result": sentinel}

        result = await proxy.get_result("boo")

        proxy_get.assert_awaited_once_with("boo")
        assert result is sentinel

    @pytest.mark.parametrize("testcase", ("success", "failure-missing-pagination"))
    async def test_get_paginated(self, testcase, proxy):
        expectation = nullcontext()

        if "success" in testcase:
            proxy.client.get.side_effect = self.get_paginated_responses()
        else:
            proxy.client.get.side_effect = self.get_paginated_responses(broken=True)
            expectation = pytest.raises(ValueError)

        with expectation:
            result = [x async for x in proxy.get_paginated("/foo")]

        if "success" in testcase:
            assert isinstance(result, list)
            assert len(result) == self.PAGINATE_TOTAL_PAGES * self.PAGINATE_PER_PAGE
            assert all(i == item["boop"] for i, item in enumerate(result))

    @pytest.mark.parametrize(
        "method, kwargs, params, expected_path, is_iterator",
        (
            ("search_users", {}, {"username": "foo"}, "/search/users/", True),
            ("get_user", {"username": "boop"}, {}, "/users/boop/", False),
            ("get_user_groups", {"username": "boop"}, {}, "/users/boop/groups/", False),
        ),
    )
    async def test_wrapper_method(self, method, kwargs, params, expected_path, is_iterator):
        fasjson_url = "http://fasjson.test"
        proxy = fasjson.FASJSONAsyncProxy(fasjson_url)
        sentinel = object()
        if is_iterator:
            proxy.get_paginated = mock.MagicMock()
            proxy.get_paginated.return_value.__aiter__.return_value = [sentinel]
        else:
            proxy.get_result = mock.AsyncMock()
            proxy.get_result.return_value = sentinel

        passed_through_kwargs = {"params": params} if params else {}

        coro = getattr(proxy, method)(**(kwargs | params))
        if is_iterator:
            retval = [x async for x in coro]
            assert retval == [sentinel]
            proxy.get_paginated.assert_called_once_with(expected_path, **passed_through_kwargs)
        else:
            retval = await coro
            assert retval is sentinel
            proxy.get_result.assert_called_once_with(expected_path, **passed_through_kwargs)


def test_get_fasjson_proxy():
    settings = mock.Mock()
    settings.services.fasjson_url = "http://foo"

    proxy = fasjson.get_fasjson_proxy(settings)

    assert str(proxy.client.base_url).rstrip("/") == "http://foo/v1"
