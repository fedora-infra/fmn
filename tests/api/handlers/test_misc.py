import pytest
from fastapi import status
from httpx import Response
from sqlalchemy.sql import text

from fmn.core.config import get_settings

from .base import BaseTestAPIV1Handler


class TestMisc(BaseTestAPIV1Handler):
    def test_get_applications(self, client):
        response = client.get(f"{self.path}/applications")

        assert response.status_code == status.HTTP_200_OK

        result = response.json()
        assert isinstance(result, list)
        assert all(isinstance(item, str) for item in result)
        # Verify list is sorted and items are unique
        assert "base" not in result
        assert result == [
            "anitya",
            "ansible",
            "bodhi",
            "ci_messages",
            "copr",
            "discourse",
            "distgit",
            "elections",
            "fedocal",
            "FMN",
            "hotness",
            "Koji",
            "mdapi",
            "noggin",
            "nuancier",
            "pagure",
            "planet",
        ]

    @pytest.mark.parametrize("ownertype", ("user", "group"))
    async def test_get_projects(self, client, respx_mocker, ownertype):
        settings = get_settings()
        settings.services.distgit_url = "http://distgit.test"

        if ownertype == "user":
            distgit_endpoint = f"{settings.services.distgit_url}/api/0/projects"
            params = {"fork": False, "short": False, "username": "dudemcpants"}
        elif ownertype == "group":
            name = "dudegroup"
            distgit_endpoint = f"{settings.services.distgit_url}/api/0/group/{name}"
            params = {"projects": True}

        distgit_json_response = {
            "pagination": {
                "pages": 1,
            },
            "projects": [
                {
                    "description": "pants containers",
                    "fullname": "containers/pants",
                    "name": "pants",
                    "namespace": "containers",
                    "access_users": {"admin": ["dudemcpants"]},
                },
                {
                    "description": "trousers rpms",
                    "fullname": "rpms/trousers",
                    "name": "trousers",
                    "namespace": "rpms",
                    "access_users": {"admin": ["dudemcpants"]},
                },
            ],
        }

        route = respx_mocker.get(distgit_endpoint, params=params).mock(
            side_effect=[
                Response(
                    status.HTTP_200_OK,
                    json=distgit_json_response,
                )
            ]
        )

        if ownertype == "user":
            response = client.get(f"{self.path}/artifacts/owned", params={"users": ["dudemcpants"]})
        elif ownertype == "group":
            response = client.get(f"{self.path}/artifacts/owned", params={"groups": ["dudegroup"]})

        assert route.called

        assert response.json() == [
            {"name": "pants", "type": "containers"},
            {"name": "trousers", "type": "rpms"},
        ]

    def test_get_projects_no_user_or_group(self, client):
        response = client.get(f"{self.path}/artifacts/owned")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_liveness(self, client):
        response = client.get(f"{self.path}/healthz/live")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"detail": "OK"}

    async def test_readiness_not_setup(self, client, db_async_session, mocker):
        await db_async_session.execute(text("DROP TABLE IF EXISTS alembic_version"))
        mocker.patch("fmn.api.database.async_session_maker", return_value=db_async_session)
        response = client.get(f"{self.path}/healthz/ready")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "no such table" in response.json()["detail"]

    async def test_readiness(self, client, db_async_schema, mocker):
        mocker.patch("fmn.api.database.async_session_maker", return_value=db_async_schema)
        response = client.get(f"{self.path}/healthz/ready")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"detail": "OK"}

    async def test_readiness_needs_upgrade(self, client, db_async_session, mocker):
        await db_async_session.execute(text("UPDATE alembic_version SET version_num='foobar'"))
        mocker.patch("fmn.api.database.async_session_maker", return_value=db_async_session)
        response = client.get(f"{self.path}/healthz/ready")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json()["detail"] == "Database schema needs to be upgraded"

    async def test_readiness_not_stamped(self, client, db_async_session, mocker):
        await db_async_session.execute(text("DELETE FROM alembic_version"))
        mocker.patch("fmn.api.database.async_session_maker", return_value=db_async_session)
        response = client.get(f"{self.path}/healthz/ready")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json()["detail"] == "Database schema needs to be upgraded"
