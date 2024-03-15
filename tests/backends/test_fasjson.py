# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
from itertools import chain
from unittest import mock

import httpx
import pytest

from fmn.backends import fasjson

from .base import BaseTestAsyncProxy


class TestFASJSONAsyncProxy(BaseTestAsyncProxy):
    CLS = fasjson.FASJSONAsyncProxy
    URL = "http://fasjson.test"
    EXPECTED_API_URL = f"{URL}/v1"

    WRAPPER_METHODS = (
        {
            "method": "search_users",
            "kwargs": {},
            "params": {"username": "foo"},
            "expected_path": "/search/users/",
        },
        {
            "method": "search_users",
            "kwargs": {},
            "params": {"username__exact": "foo"},
            "expected_path": "/search/users/",
        },
        {
            "method": "get_user",
            "kwargs": {"username": "boop"},
            "params": {},
            "expected_path": "/users/boop/",
        },
        {
            "method": "get_user_groups",
            "kwargs": {"username": "boop"},
            "params": {},
            "expected_path": "/users/boop/groups/",
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
            assert params["page_number"] == 2
        else:
            assert next_url is None

    async def test_get_user_groups_failure(self, respx_mocker, proxy_unmocked_client):
        route = respx_mocker.get(f"{self.expected_api_url}/users/boop/groups/").mock(
            side_effect=httpx.Response(status_code=500)
        )

        response = await proxy_unmocked_client.get_user_groups(username="boop")
        assert route.called
        assert response == []

    async def test_get_user_404(self, respx_mocker, proxy_unmocked_client):
        route = respx_mocker.get(f"{self.expected_api_url}/users/boop/").mock(
            side_effect=httpx.Response(status_code=404)
        )
        response = await proxy_unmocked_client.get_user(username="boop")
        assert route.called
        assert response is None

    async def test_get_user_failure(self, respx_mocker, proxy_unmocked_client):
        route = respx_mocker.get(f"{self.expected_api_url}/users/boop/").mock(
            side_effect=httpx.Response(status_code=500)
        )
        with pytest.raises(httpx.HTTPStatusError):
            await proxy_unmocked_client.get_user(username="boop")
        assert route.called

    @pytest.mark.parametrize(
        "testcase",
        chain(
            (
                pytest.param((testcase, topic), id=f"{testcase}-{topic}")
                for testcase in ("success", "failure-missing-user")
                for topic in ("group.member.sponsor", "user.create", "user.update")
            ),
            (
                "skip-other-topic",
                "success-ish-with-exceptions",
            ),
        ),
    )
    async def test_invalidate_on_message(self, mocker, testcase, proxy, caplog):
        cache = mocker.patch("fmn.backends.fasjson.cache")
        cache.delete_tags = mock.AsyncMock()

        if isinstance(testcase, tuple):
            testcase, topic = testcase
        else:
            topic = "user.create"

        if "with-exceptions" in testcase:
            cache.delete_tags.side_effect = RuntimeError("BOO")

        # basic (incomplete) message
        message = mock.Mock(
            topic=f"org.fedoraproject.prod.fas.{topic}", body={"msg": {"user": "testuser"}}
        )
        body = message.body
        user = body["msg"]["user"]

        # Complete the message or muck it up, depending on testcase.
        if "failure-missing-user" in testcase:
            del body["msg"]["user"]

        if "skip-other-topic" in testcase:
            message.topic = "this.is.not.the.message.you’re.looking.for"

        with caplog.at_level(logging.DEBUG):
            await proxy.invalidate_on_message(message, None)

        if "success" not in testcase:
            cache.delete_tags.assert_not_called()

            if "missing-user" in testcase:
                assert "No information found about affected user" in caplog.text
            elif "other-topic" in testcase:
                assert "Skipping message with topic" in caplog.text
        else:
            assert cache.delete_tags.awaited_once()
            args, _ = cache.delete_tags.await_args
            assert set(args) == {
                "fasjson:search_users:username__exact=",
                f"fasjson:search_users:username__exact={user}",
                f"fasjson:get_user:username={user}",
                f"fasjson:get_user_groups:username={user}",
            }

            if "with-exceptions" in testcase:
                assert "Deleting cache entries yielded an exception:" in caplog.text


@mock.patch("fmn.backends.fasjson.get_settings")
def test_get_fasjson_proxy(get_settings):
    settings = mock.Mock()
    settings.services.fasjson_url = "http://foo"
    get_settings.return_value = settings

    proxy = fasjson.get_fasjson_proxy()
    assert str(proxy.client.base_url).rstrip("/") == "http://foo/v1"

    cached_proxy = fasjson.get_fasjson_proxy()
    assert cached_proxy is proxy

    get_settings.assert_called_once_with()
