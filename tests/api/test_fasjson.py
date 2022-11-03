from contextlib import nullcontext
from unittest import mock

import pytest

from fmn.api import fasjson


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

    @pytest.mark.parametrize("testcase", ("single", "paginated", "broken"))
    async def test_get(self, testcase):
        fasjson_url = "http://fasjson.test"
        proxy = fasjson.FASJSONAsyncProxy(fasjson_url)
        proxy.client = client = mock.AsyncMock()

        expectation = nullcontext()

        if "single" in testcase:
            response = mock.Mock()
            response.json.return_value = {"result": {"boop": "yes"}}
            client.get.return_value = response
        elif "paginated" in testcase:
            client.get.side_effect = self.get_paginated_responses()
        elif "broken" in testcase:
            client.get.side_effect = self.get_paginated_responses(broken=True)
            expectation = pytest.raises(RuntimeError)

        with expectation:
            result = await proxy.get("/foo")

        if "single" in testcase:
            assert result == {"boop": "yes"}
        elif "paginated" in testcase:
            assert isinstance(result, list)
            assert len(result) == self.PAGINATE_TOTAL_PAGES * self.PAGINATE_PER_PAGE
            assert all(i == item["boop"] for i, item in enumerate(result))

    @pytest.mark.parametrize(
        "method, processed_kwargs, passed_through_kwargs, expected_path",
        (
            ("search_users", {}, {"username": "foo"}, "/search/users/"),
            ("get_user", {"username": "boop"}, {}, "/users/boop/"),
            ("list_user_groups", {"username": "boop"}, {}, "/users/boop/groups/"),
        ),
    )
    def test_wrapper_method(self, method, processed_kwargs, passed_through_kwargs, expected_path):
        fasjson_url = "http://fasjson.test"
        proxy = fasjson.FASJSONAsyncProxy(fasjson_url)
        proxy.get = mock.Mock()
        proxy.get.return_value = sentinel = object()

        retval = getattr(proxy, method)(**(processed_kwargs | passed_through_kwargs))

        assert retval is sentinel
        proxy.get.assert_called_once_with(expected_path, **passed_through_kwargs)


def test_get_fasjson_proxy():
    settings = mock.Mock()
    settings.services.fasjson_url = "http://foo"

    proxy = fasjson.get_fasjson_proxy(settings)

    assert str(proxy.client.base_url).rstrip("/") == "http://foo/v1"
