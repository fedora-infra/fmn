import re

import httpx
import pytest
from fastapi import status
from httpx import Response
from sqlalchemy.sql import text

from fmn.api.handlers.utils import get_last_messages
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


class TestPreviewRule(BaseTestAPIV1Handler):
    _dummy_rule_dict = rule = {
        "tracking_rule": {
            "name": "artifacts-followed",
            "params": [{"type": "rpms", "name": "foobar"}],
        },
        "generation_rules": [
            {
                "filters": {
                    "applications": ["koji"],
                }
            }
        ],
    }

    def test_preview_basic(self, respx_mocker, client, api_identity, make_mocked_message):
        respx_mocker.get(
            "https://apps.fedoraproject.org/datagrepper/v2/search?rows_per_page=100&delta=3600"
        ).mock(
            httpx.Response(
                status.HTTP_200_OK,
                json={
                    "raw_messages": [
                        {
                            "id": "id-foobar",
                            "topic": "topic.foobar",
                            "headers": {
                                "fedora_messaging_schema": "testmessage",
                                "sent-at": "2022-01-01T00:00:00+00:00",
                            },
                            "body": {"app": "koji", "packages": ["foobar"]},
                        }
                    ],
                    "pages": 1,
                },
            )
        )

        response = client.post(f"{self.path}/rule-preview", json=self._dummy_rule_dict)

        assert response.status_code == status.HTTP_200_OK

        result = response.json()
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["protocol"] == "preview"
        assert result[0]["content"] == {
            "date": "2022-01-01T00:00:00+00:00",
            "topic": "topic.foobar",
            "summary": "Message on topic.foobar",
            "priority": 0,
            "application": "koji",
            "author": None,
        }

    def test_preview_anonymous(self, client, api_identity):
        api_identity.name = None
        response = client.post(f"{self.path}/rule-preview", json=self._dummy_rule_dict)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_dg_url_fix(self, mocker, respx_mocker):
        settings = get_settings()
        settings.services.datagrepper_url = "http://datagrepper.test"
        mocker.patch("fmn.api.handlers.utils.get_settings", return_value=settings)
        resp = respx_mocker.get(re.compile(r"http://datagrepper\.test/v2/search.*")).mock(
            httpx.Response(status.HTTP_200_OK, json={"raw_messages": [], "pages": 0})
        )
        messages = [m async for m in get_last_messages(1)]
        assert messages == []
        assert resp.call_count == 1

    async def test_get_last_messages_pages(self, mocker, respx_mocker, make_mocked_message):
        rsp1 = respx_mocker.get(
            "https://apps.fedoraproject.org/datagrepper/v2/search?rows_per_page=100&delta=3600"
        ).mock(
            httpx.Response(
                status.HTTP_200_OK,
                json={
                    "raw_messages": [
                        {
                            "id": "id-foobar-1",
                            "topic": "topic.foobar",
                            "headers": {
                                "fedora_messaging_schema": "testmessage",
                                "sent-at": "2022-01-01T00:00:00+00:00",
                            },
                            "body": {"app": "koji", "packages": ["foobar"]},
                        }
                    ],
                    "arguments": {"page": 1},
                    "pages": 2,
                },
            )
        )
        rsp2 = respx_mocker.get(
            "https://apps.fedoraproject.org/datagrepper/v2/search?"
            "page=2&rows_per_page=100&delta=3600"
        ).mock(
            httpx.Response(
                status.HTTP_200_OK,
                json={
                    "raw_messages": [
                        {
                            "id": "id-foobar-2",
                            "topic": "topic.foobar",
                            "headers": {
                                "fedora_messaging_schema": "testmessage",
                                "sent-at": "2022-01-01T00:00:00+00:00",
                            },
                            "body": {"app": "koji", "packages": ["foobar"]},
                        }
                    ],
                    "arguments": {"page": 2},
                    "pages": 2,
                },
            )
        )

        messages = [m async for m in get_last_messages(1)]

        assert len(messages) == 2
        assert rsp1.call_count == 1
        assert rsp2.call_count == 1
