# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from contextlib import nullcontext
from unittest import mock

import httpx
import pytest

from fmn.backends import base


class ConcreteAPIClient(base.APIClient):
    payload_field = "result"

    def determine_next_page_params(self, url, params, result):
        page_number = result["page"]["page_number"]
        if page_number >= result["page"]["total_pages"]:
            return None, None

        new_params = params.copy()
        new_params["page_number"] = page_number + 1
        return url, new_params


@pytest.fixture
def client():
    client = ConcreteAPIClient()
    client.client = mock.AsyncMock()
    return client


class TestAPIClient:
    PAGINATE_TOTAL_PAGES = 5
    PAGINATE_PER_PAGE = 5

    @pytest.mark.parametrize("with_base_url", (True, False))
    def test___init__(self, with_base_url):
        if with_base_url:
            kwargs = {"base_url": "https://example.com"}
        else:
            kwargs = {}
        client = ConcreteAPIClient(**kwargs)
        assert isinstance(client.client, httpx.AsyncClient)
        if with_base_url:
            assert client.client.base_url == "https://example.com"
        else:
            assert client.client.base_url == ""

    @pytest.mark.parametrize("initialized_with_trailing_slash", (True, False))
    def test_base_url_with_trailing_slash(self, initialized_with_trailing_slash):
        base_url = "https://foo"
        expected_result = base_url + "/"
        if initialized_with_trailing_slash:
            base_url += "/"

        client = ConcreteAPIClient(base_url)

        assert client.base_url_with_trailing_slash == expected_result

    def test_api_url(self):
        base_url = "https://foo"
        assert ConcreteAPIClient(base_url).api_url == base_url

    def test___str__(self):
        client = ConcreteAPIClient("https://example.com")
        assert str(client) == "ConcreteAPIClient(https://example.com)"

    @pytest.mark.parametrize("testcase", ("set-on-call", "set-on-class", "unset"))
    def test_extract_payload(self, testcase):
        test_result = {
            "result": "result",
            "foo": "foo",
        }

        if testcase == "set-on-call":
            kwargs = {"payload_field": "foo"}
        else:
            kwargs = {}

        if testcase == "unset":

            class UnsetAPIClient(base.APIClient):
                def determine_next_page_params(self, url, params, result):
                    pass

            client = UnsetAPIClient()
        else:
            client = ConcreteAPIClient()

        payload = client.extract_payload(test_result, **kwargs)

        if testcase == "set-on-call":
            assert payload == "foo"
        elif testcase == "set-on-class":
            assert payload == "result"
        else:
            assert payload == test_result

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
        if broken == "missing-pagination":
            pages[-1] = {"result": {"this is": "broken"}}
        elif broken == "pagination-recursion":
            pages[-1]["page"]["page_number"] -= 1
        return pages

    @classmethod
    def get_paginated_responses(cls, broken=False):
        responses = []

        for result in cls.get_paginated_results(broken=broken):
            response = mock.Mock()
            response.json.return_value = result
            responses.append(response)

        return responses

    async def test_get(self, client):
        client.client.get.return_value = response = mock.Mock()
        response.json.return_value = sentinel = object()

        result = await client.get("url", foo="bar")

        client.client.get.assert_awaited_once_with("url", foo="bar")
        response.raise_for_status.assert_called_once_with()
        assert result is sentinel

    async def test_get_payload(self, client):
        with mock.patch.object(client, "get") as client_get:
            client_get.return_value = {"result": "boo"}

            result = await client.get_payload("https://boo.test")

            client_get.assert_awaited_once_with("https://boo.test")
            assert result == "boo"

    @pytest.mark.parametrize(
        "testcase",
        (
            "success",
            "success-with-params",
            "failure-missing-pagination",
            "failure-pagination-recursion",
        ),
    )
    async def test_get_paginated(self, testcase, client):
        expectation = nullcontext()

        if "success" in testcase:
            client.client.get.side_effect = self.get_paginated_responses()
        else:
            if "missing-pagination" in testcase:
                client.client.get.side_effect = self.get_paginated_responses(
                    broken="missing-pagination"
                )
                expectation = pytest.raises(KeyError)
            if "pagination-recursion" in testcase:
                client.client.get.side_effect = self.get_paginated_responses(
                    broken="pagination-recursion"
                )
                expectation = pytest.raises(base.PaginationRecursionError)

        if "with-params" in testcase:
            kwargs = {"params": {"foo": "bar"}}
        else:
            kwargs = {}

        with expectation:
            result = [x async for x in client.get_paginated("/foo", **kwargs)]

        if "success" in testcase:
            assert isinstance(result, list)
            assert len(result) == self.PAGINATE_TOTAL_PAGES * self.PAGINATE_PER_PAGE
            assert all(i == item["boop"] for i, item in enumerate(result))


@pytest.mark.parametrize("testcase", ("success", "raises-exception"))
async def test_handle_http_error(testcase, mocker):
    async def fn_to_be_decorated():
        if "raises-exception" in testcase:
            raise httpx.HTTPStatusError(
                "Boo.", request=None, response=httpx.Response(status_code=404)
            )
        else:
            return ["item"]

    decorated_fn = base.handle_http_error(list)(fn_to_be_decorated)

    result = await decorated_fn()

    if "success" in testcase:
        assert result == ["item"]
    else:
        assert result == []
