import logging

from fastapi import Depends
from httpx import AsyncClient

from ..core.config import Settings, get_settings

log = logging.getLogger(__name__)


class DistGitClient:
    def __init__(self, settings):
        self.client = AsyncClient(base_url=settings.services.distgit_url, timeout=None)

    async def get_projects(self, pattern):
        response = await self.client.get(
            "/api/0/projects",
            params={
                "pattern": f"*{pattern}*",
                "short": "true",
                "fork": "false",
            },
        )
        response.raise_for_status()
        result = response.json()

        return [project["name"] for project in result["projects"]]


def get_distgit_client(settings: Settings = Depends(get_settings)):
    return DistGitClient(settings)
