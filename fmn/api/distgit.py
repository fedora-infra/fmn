import logging
from urllib.parse import urlencode

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
        return result["projects"]

    async def get_owned(self, names, user_or_group):
        def _append_artifacts(projects):
            for p in projects:
                artifacts.append({"type": p["namespace"], "name": p["name"]})

        artifacts = []
        endpoint = "/api/0/projects"
        for name in names:
            params = {"short": "true", "fork": "false"}

            if user_or_group == "user":
                params["owner"] = name
            elif user_or_group == "group":
                params["username"] = f"@{name}"
            else:
                raise ValueError("Argument user_or_group must be either user or group")

            params["page"] = "1"
            url = f"{endpoint}?{urlencode(params)}"

            while url:
                response = await self.client.get(url)
                response.raise_for_status()
                data = response.json()
                _append_artifacts(data["projects"])
                url = data.get("pagination", {}).get("next")

        return artifacts


def get_distgit_client(settings: Settings = Depends(get_settings)):
    return DistGitClient(settings)
