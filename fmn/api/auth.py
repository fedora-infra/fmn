# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import logging
import time
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from httpx import AsyncClient, HTTPError
from pydantic import BaseModel, ConfigDict
from pydantic.fields import ModelPrivateAttr

from ..core.config import get_settings

log = logging.getLogger(__name__)


class TokenExpired(ValueError):
    pass


_token_to_identities_cache: dict[str, "Identity"] = dict()
_cache_next_gc_after: int | None = None


class Identity(BaseModel):
    model_config = ConfigDict(extra="ignore")

    _client: AsyncClient | None = None

    name: str
    admin: bool
    expires_at: float
    user_info: dict[str, Any]

    @classmethod
    def client(cls) -> AsyncClient:
        settings = get_settings()
        if isinstance(cls._client, ModelPrivateAttr):
            cls._client = AsyncClient(
                base_url=settings.oidc_provider_url,
                timeout=None,
            )
        return cls._client

    @classmethod
    def _cache_collect_garbage(cls, force: bool = False) -> None:
        global _token_to_identities_cache, _cache_next_gc_after
        id_cache_gc_interval = get_settings().id_cache_gc_interval
        now = time.time()
        then = now + id_cache_gc_interval

        if not force:
            if not _cache_next_gc_after:
                _cache_next_gc_after = then
                return

            if now < _cache_next_gc_after:
                return

        _token_to_identities_cache = {
            k: v for k, v in _token_to_identities_cache.items() if v.expires_at > now
        }
        _cache_next_gc_after = then

    @classmethod
    async def from_oidc_token(cls, token: str) -> "Identity":
        identity = _token_to_identities_cache.get(token)
        if not identity:
            settings = get_settings()
            token_info_response = await cls.client().post(
                settings.oidc_token_info_url,
                data={
                    "token": token,
                    "client_id": settings.oidc_client_id,
                    "client_secret": settings.oidc_client_secret,
                },
            )
            token_info_response.raise_for_status()
            token_info_result = token_info_response.json()

            user_info_response = await cls.client().post(
                settings.oidc_user_info_url, data={"access_token": token}
            )
            user_info_response.raise_for_status()
            user_info_result = user_info_response.json()

            identity = cls(
                name=token_info_result["username"],
                admin=any(
                    g in get_settings().admin_groups for g in user_info_result.get("groups", [])
                ),
                expires_at=float(token_info_result["exp"]),
                user_info=user_info_result,
            )

        if identity.expires_at < time.time():
            cls._cache_collect_garbage(force=True)
            raise TokenExpired(token)
        else:
            cls._cache_collect_garbage()

        _token_to_identities_cache[token] = identity

        return identity


class IdentityFactory:
    def __init__(self, optional=False):
        self.optional = optional

    async def process_oidc_auth(
        self, creds: HTTPAuthorizationCredentials | None
    ) -> Identity | None:
        if not creds:
            return None
        return await Identity.from_oidc_token(creds.credentials)

    async def __call__(
        self, bearer: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False))
    ) -> Identity | None:
        try:
            identity = await self.process_oidc_auth(bearer)
        except TokenExpired as exc:
            if self.optional:
                return None
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Token expired") from exc
        except HTTPError as exc:
            if self.optional:
                return None
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, detail=f"Could not get user information: {exc}"
            ) from exc
        if identity is None and not self.optional:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        return identity


get_identity = IdentityFactory(optional=False)
get_identity_optional = IdentityFactory(optional=True)


async def get_identity_admin(identity: Identity = Depends(get_identity)):
    if not identity.admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not an admin")
    return identity
