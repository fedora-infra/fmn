import pytest

from fmn.backends import datagrepper

from .base import BaseTestAsyncProxy


class TestDatagrepperAsyncProxy(BaseTestAsyncProxy):
    CLS = datagrepper.DatagrepperAsyncProxy
    URL = "https://datagrepper.test"
    WRAPPER_METHODS = (
        {
            "method": "search",
            "kwargs": {},
            "params": {"delta": 3600},
            "expected_path": "/search",
            "is_iterator": True,
        },
    )

    @pytest.mark.parametrize("testcase", ("normal", "last-page", "pagination-missing"))
    def test_determine_next_page_params(self, testcase, proxy):
        page = 1
        if "last-page" in testcase:
            page = 2

        if "pagination-missing" in testcase:
            result = {}
        else:
            result = {"arguments": {"page": page}, "pages": 2}

        params = {}

        next_url, params = proxy.determine_next_page_params("/boo", params=params, result=result)

        if "normal" in testcase:
            assert next_url == "/boo"
            assert params["page"] == 2
        else:
            assert next_url is None
