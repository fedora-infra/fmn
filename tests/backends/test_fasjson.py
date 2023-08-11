# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import asyncio
import logging
import re
from itertools import chain
from unittest import mock

import httpx
import pytest

from fmn.backends import fasjson
from fmn.cache.util import get_pattern_for_cached_calls

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
        cache.delete = mock.AsyncMock()

        asyncio_create_task = mocker.patch.object(asyncio, "create_task", wraps=asyncio.create_task)
        asyncio_gather = mocker.patch.object(asyncio, "gather", wraps=asyncio.gather)

        if isinstance(testcase, tuple):
            testcase, topic = testcase
        else:
            topic = "user.create"

        if "with-exceptions" in testcase:
            # 4 keys to delete, let's muck up the last
            cache.delete.side_effect = [object(), object(), object(), RuntimeError("BOO")]

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

        # Make up cache keys to be deleted

        async def mocked_cache_get_match(pattern):
            kwargs = {"self": proxy}

            if ".search_users:" in pattern:
                func = proxy.search_users
                kwargs["username__exact"] = None if ":username__exact::" in pattern else user
            elif ".get_user:" in pattern:
                func = proxy.get_user
                kwargs["username"] = user
            elif ".get_user_groups:" in pattern:
                func = proxy.get_user_groups
                kwargs["username"] = user

            key = get_pattern_for_cached_calls(func, **kwargs)[0]

            yield key, None

        cache.get_match.side_effect = mocked_cache_get_match

        with caplog.at_level(logging.DEBUG):
            await proxy.invalidate_on_message(message, None)

        if "success" not in testcase:
            asyncio_create_task.assert_not_called()
            asyncio_gather.assert_not_called()
            cache.delete.assert_not_called()

            if "missing-user" in testcase:
                assert "No information found about affected user" in caplog.text
            elif "other-topic" in testcase:
                assert "Skipping message with topic" in caplog.text
        else:
            assert any(
                f":FASJSONAsyncProxy.search_users:self:{proxy}:" in call.args[0]
                and ":username__exact::" in call.args[0]
                for call in cache.delete.await_args_list
            )
            assert any(
                f":FASJSONAsyncProxy.search_users:self:{proxy}:" in call.args[0]
                and f":username__exact:{user}:" in call.args[0]
                for call in cache.delete.await_args_list
            )
            assert any(
                f":FASJSONAsyncProxy.get_user:self:{proxy}:" in call.args[0]
                and re.search(rf":username:{user}(?::|$)", call.args[0])
                for call in cache.delete.await_args_list
            )
            assert any(
                f":FASJSONAsyncProxy.get_user_groups:self:{proxy}:" in call.args[0]
                and re.search(rf":username:{user}(?::|$)", call.args[0])
                for call in cache.delete.await_args_list
            )
            assert len(cache.delete.await_args_list) == 4

            if "with-exceptions" in testcase:
                assert "Deleting 4 cache entries yielded 1 exception(s):" in caplog.text


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
