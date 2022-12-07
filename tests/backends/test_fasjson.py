import pytest

from fmn.backends import fasjson

from .base import BaseTestAsyncProxy


class TestFASJSONAsyncProxy(BaseTestAsyncProxy):

    CLS = fasjson.FASJSONAsyncProxy
    URL = "http://fasjson.test"
    EXPECTED_BASE_URL = f"{URL}/v1/"

    WRAPPER_METHODS = (
        {
            "method": "search_users",
            "kwargs": {},
            "params": {"username": "foo"},
            "expected_path": "/search/users/",
            "is_iterator": True,
        },
        {
            "method": "get_user",
            "kwargs": {"username": "boop"},
            "params": {},
            "expected_path": "/users/boop/",
            "is_iterator": False,
        },
        {
            "method": "get_user_groups",
            "kwargs": {"username": "boop"},
            "params": {},
            "expected_path": "/users/boop/groups/",
            "is_iterator": False,
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
            result = {"page": {"page_number": page, "total_pages": 2}}

        params = {}

        next_url, params = proxy.determine_next_page_params("/boo", params=params, result=result)

        if "normal" in testcase:
            assert next_url == "/boo"
            assert params["page"] == 2
        else:
            assert next_url is None
