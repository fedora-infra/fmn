# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import time
from contextlib import nullcontext
from unittest import mock

import pytest
from fastapi import HTTPException, status
from httpx import AsyncClient, HTTPError

from fmn.api import auth


@pytest.fixture
def mock_client(mocker):
    mocker.patch.object(auth, "_cache_next_gc_after", new=None)
    mocker.patch.object(auth, "_token_to_identities_cache", new_callable=dict)
    client_factory = mocker.patch.object(auth.Identity, "client")
    client = client_factory.return_value = mock.AsyncMock()
    client.post.return_value.raise_for_status = mock.Mock()
    client.post.return_value.json = mock.Mock()
    return client


class TestIdentity:
    def test_client(self):
        client = auth.Identity.client()
        assert isinstance(client, AsyncClient)

        new_client = auth.Identity.client()
        assert new_client is client

    @pytest.mark.parametrize("expired", (False, True))
    @pytest.mark.parametrize("perform_gc", (False, True))
    async def test_from_oidc_token(self, mock_client, expired, perform_gc):
        now = time.time()
        if expired:
            expectation = pytest.raises(auth.TokenExpired)
            then = now - 1
        else:
            expectation = nullcontext()
            then = now + 3600

        token_info_result = {"username": "karlheinzschinkenwurst", "exp": str(then)}
        user_info_result = {
            "email": "karlheinz@schinkenwurst.org",
            "groups": ["users", "admins"],
            "name": "Karl-Heinz Schinkenwurst",
            "nickname": "karlheinzschinkenwurst",
            "preferred_username": "karlheinzschinkenwurst",
        }
        mock_client.post.return_value.json.side_effect = [
            token_info_result,
            user_info_result if not expired else {},
        ]

        # cold cache

        with expectation:
            identity = await auth.Identity.from_oidc_token("abcd-1234")

        assert mock_client.post.await_count == 2

        if expired:
            return

        assert identity.name == token_info_result["username"]
        assert str(identity.expires_at) == token_info_result["exp"]
        assert identity.user_info == user_info_result

        # hot cache

        mock_client.post.reset_mock()

        auth._token_to_identities_cache["efgh-5678"] = gc_sentinel = mock.Mock(expires_at=now - 1)

        if perform_gc:
            auth._cache_next_gc_after = now - 1

        identity2 = await auth.Identity.from_oidc_token("abcd-1234")

        mock_client.post.assert_not_awaited()
        assert identity2 is identity

        if perform_gc:
            assert gc_sentinel not in auth._token_to_identities_cache.values()
        else:
            assert gc_sentinel in auth._token_to_identities_cache.values()


class TestIdentityFactory:
    @mock.patch.object(auth.Identity, "from_oidc_token")
    async def test_process_oidc_auth(self, from_oidc_token):
        from_oidc_token.return_value = sentinel = object()
        creds = mock.Mock(credentials="dead-beef")
        identity = await auth.IdentityFactory().process_oidc_auth(creds=creds)

        assert identity is sentinel
        from_oidc_token.assert_awaited_once_with("dead-beef")

    @pytest.mark.parametrize("testcase", ("success", "failure-mandatory", "failure-optional"))
    async def test___call__(self, testcase):
        optional = "optional" in testcase
        success = "success" in testcase

        factory = auth.IdentityFactory(optional=optional)

        with mock.patch.object(factory, "process_oidc_auth") as process_oidc_auth:
            expectation = nullcontext()
            if success:
                process_oidc_auth.return_value = result_sentinel = object()
            else:
                process_oidc_auth.side_effect = auth.TokenExpired("abcd-1234")
                if not optional:
                    expectation = pytest.raises(HTTPException)

            if success:
                bearer_sentinel = object()
                args = (bearer_sentinel,)
            else:
                args = (None,)

            with expectation as excinfo:
                result = await factory(*args)

            if success:
                process_oidc_auth.assert_awaited_once_with(bearer_sentinel)
            else:
                process_oidc_auth.assert_awaited_once_with(None)
                if not optional:
                    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED

            if success:
                assert result is result_sentinel
            elif optional:
                assert result is None

    async def test___call__anon(self):
        factory = auth.IdentityFactory(optional=True)
        result = await factory(None)
        assert result is None

    async def test___call__anon_mandatory(self):
        factory = auth.IdentityFactory(optional=False)
        with pytest.raises(HTTPException) as excinfo:
            await factory(None)
        assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED

    async def test___call__request_failure(self):
        factory = auth.IdentityFactory(optional=False)
        factory.process_oidc_auth = mock.Mock(side_effect=HTTPError("dummy error"))
        with pytest.raises(HTTPException) as excinfo:
            await factory(None)
        assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert excinfo.value.detail == "Could not get user information: dummy error"

    async def test___call__request_failure_optional(self):
        factory = auth.IdentityFactory(optional=True)
        factory.process_oidc_auth = mock.Mock(side_effect=HTTPError("dummy error"))
        result = await factory(None)
        assert result is None
