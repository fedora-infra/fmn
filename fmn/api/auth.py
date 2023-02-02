import logging
import time

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from httpx import AsyncClient
from pydantic import BaseModel

from ..core.config import get_settings

log = logging.getLogger(__name__)


class TokenExpired(ValueError):
    pass


class Identity(BaseModel):
    _client = None
    _token_to_identities_cache = {}
    _cache_next_gc_after = None

    name: str
    expires_at: float

    class Config:
        extra = "ignore"

    @classmethod
    def client(cls) -> AsyncClient:
        settings = get_settings()
        if not cls._client:
            cls._client = AsyncClient(
                base_url=settings.oidc_provider_url,
                timeout=None,
            )
        return cls._client

    @classmethod
    def _cache_collect_garbage(cls, force: bool = False) -> None:
        id_cache_gc_interval = get_settings().id_cache_gc_interval
        now = time.time()
        then = now + id_cache_gc_interval

        if not force:
            if not cls._cache_next_gc_after:
                cls._cache_next_gc_after = then
                return

            if now < cls._cache_next_gc_after:
                return

        cls._token_to_identities_cache = {
            k: v for k, v in cls._token_to_identities_cache.items() if v.expires_at > now
        }
        cls._cache_next_gc_after = then

    @classmethod
    async def from_oidc_token(cls, token: str) -> "Identity":
        identity = cls._token_to_identities_cache.get(token)
        if not identity:
            settings = get_settings()
            response = await cls.client().post(
                settings.oidc_token_info_url,
                data={
                    "token": token,
                    "client_id": settings.oidc_client_id,
                    "client_secret": settings.oidc_client_secret,
                },
            )
            response.raise_for_status()
            result = response.json()

            identity = cls(name=result["username"], expires_at=float(result["exp"]))

        if identity.expires_at < time.time():
            cls._cache_collect_garbage(force=True)
            raise TokenExpired(token)
        else:
            cls._cache_collect_garbage()

        cls._token_to_identities_cache[token] = identity

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
            return await self.process_oidc_auth(bearer)
        except TokenExpired as exc:
            if self.optional:
                return None
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Token expired") from exc


get_identity = IdentityFactory(optional=False)
get_identity_optional = IdentityFactory(optional=True)
