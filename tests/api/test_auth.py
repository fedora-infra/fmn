import time
from contextlib import nullcontext
from unittest import mock

import pytest
from fastapi import HTTPException, status
from httpx import AsyncClient

from fmn.api.auth import Identity, IdentityFactory, TokenExpired


class TestIdentity:
    def test_client(self):
        client = Identity.client()
        assert isinstance(client, AsyncClient)

        new_client = Identity.client()
        assert new_client is client

    @pytest.mark.parametrize("expired", (False, True))
    @pytest.mark.parametrize("perform_gc", (False, True))
    @mock.patch.object(Identity, "_cache_next_gc_after", new=None)
    @mock.patch.object(Identity, "_token_to_identities_cache", new_callable=dict)
    @mock.patch.object(Identity, "client")
    async def test_from_oidc_token(self, client, _token_to_identities_cache, expired, perform_gc):
        now = time.time()
        if expired:
            expectation = pytest.raises(TokenExpired)
            then = now - 1
        else:
            expectation = nullcontext()
            then = now + 3600

        client.return_value = mock_client = mock.AsyncMock()
        mock_client.post.return_value.raise_for_status = mock.Mock()
        mock_client.post.return_value.json = mock.Mock()
        mock_client.post.return_value.json.return_value = token_info_result = {
            "username": "karlheinzschinkenwurst",
            "exp": str(then),
        }

        # cold cache

        with expectation:
            identity = await Identity.from_oidc_token("abcd-1234")

        mock_client.post.assert_awaited_once()

        if expired:
            return

        assert identity.name == token_info_result["username"]
        assert str(identity.expires_at) == token_info_result["exp"]

        # hot cache

        mock_client.post.reset_mock()

        Identity._token_to_identities_cache["efgh-5678"] = gc_sentinel = mock.Mock(
            expires_at=now - 1
        )

        if perform_gc:
            Identity._cache_next_gc_after = now - 1

        identity2 = await Identity.from_oidc_token("abcd-1234")

        mock_client.post.assert_not_awaited()
        assert identity2 is identity

        if perform_gc:
            assert gc_sentinel not in Identity._token_to_identities_cache.values()
        else:
            assert gc_sentinel in Identity._token_to_identities_cache.values()


class TestIdentityFactory:
    @mock.patch.object(Identity, "from_oidc_token")
    async def test_process_oidc_auth(self, from_oidc_token):
        from_oidc_token.return_value = sentinel = object()
        creds = mock.Mock(credentials="dead-beef")
        identity = await IdentityFactory().process_oidc_auth(creds=creds)

        assert identity is sentinel
        from_oidc_token.assert_awaited_once_with("dead-beef")

    @pytest.mark.parametrize("testcase", ("success", "failure-mandatory", "failure-optional"))
    async def test___call__(self, testcase):
        optional = "optional" in testcase
        success = "success" in testcase

        factory = IdentityFactory(optional=optional)

        with mock.patch.object(factory, "process_oidc_auth") as process_oidc_auth:
            expectation = nullcontext()
            if success:
                process_oidc_auth.return_value = result_sentinel = object()
            else:
                process_oidc_auth.side_effect = TokenExpired("abcd-1234")
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
        factory = IdentityFactory(optional=True)
        result = await factory(None)
        assert result is None
