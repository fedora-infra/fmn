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
            result_next = "/boo?page=2"
        else:
            result_next = None

        if "pagination-missing" in testcase:
            result = {}
        else:
            result = {"pagination": {"next": result_next}}

        params_sentinel = object()

        next_url, params = proxy.determine_next_page_params(
            "/boo", params=params_sentinel, result=result
        )

        if "normal" in testcase:
            assert next_url == result_next
            assert params is params_sentinel
        else:
            assert next_url is None
