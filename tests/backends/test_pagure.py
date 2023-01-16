import pytest

from fmn.backends import pagure

from .base import BaseTestAsyncProxy


class TestPagureAsyncProxy(BaseTestAsyncProxy):
    CLS = pagure.PagureAsyncProxy
    URL = "https://pagure.test"
    EXPECTED_BASE_URL = f"{URL}/api/0/"

    @pytest.mark.parametrize("testcase", ("normal", "last-page", "pagination-missing"))
    def test_determine_next_page_params(self, testcase, proxy):
        if "normal" in testcase:
            expected_next_url = "/boo"
        else:
            expected_next_url = None

        if "pagination-missing" in testcase:
            result = {}
        elif "last-page" in testcase:
            result = {"pagination": {"next": None}}
        else:
            result = {"pagination": {"next": "/boo?page=2"}}

        params = {}

        next_url, next_params = proxy.determine_next_page_params(
            "/boo", params=params, result=result
        )

        if "normal" in testcase:
            assert next_url == expected_next_url
            assert next_params == params | {"page": "2"}
        else:
            assert next_url is None
            assert next_params is None
