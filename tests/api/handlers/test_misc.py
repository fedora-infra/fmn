# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from unittest import mock

import pytest
from fastapi import status
from httpx import Response
from sqlalchemy.sql import text

from fmn.core.config import get_settings

from .base import BaseTestAPIV1Handler


class TestMisc(BaseTestAPIV1Handler):
    def test_get_applications(self, client):
        EXPECTED_APPS = {
            appname.lower()
            for appname in (
                "anitya",
                "ansible",
                "bodhi",
                "ci_messages",
                "copr",
                "discourse",
                "distgit",
                "elections",
                "FAS",
                "fedocal",
                "FMN",
                "hotness",
                "Koji",
                "mdapi",
                "nuancier",
                "pagure",
                "planet",
            )
        }

        response = client.get(f"{self.path}/applications")

        assert response.status_code == status.HTTP_200_OK

        result = response.json()

        assert isinstance(result, list)
        assert all(isinstance(item, str) for item in result)
        assert "base" not in result

        result_lower = [appname.lower() for appname in result]

        # Verify list is sorted and items are unique
        assert result_lower == sorted(set(result_lower))

        # Verify all expected apps are present
        assert EXPECTED_APPS <= set(result_lower)

    def test_get_applications_normalize_case(self, mocker, client):
        metadata = mocker.patch("fmn.api.handlers.misc.metadata")
        metadata.entry_points.return_value = entry_points = mock.Mock()

        eps = []
        for msg_topic, msg_cls_app_name in (
            ("blub.unused.what", None),
            ("blub.build.started", "Blub"),
            ("abc.something", "abc"),
        ):
            ep = mock.Mock()
            ep.name = msg_topic
            ep.load.return_value = msg_cls = mock.Mock()
            msg_cls.app_name.fget.return_value = msg_cls_app_name
            eps.append(ep)

        entry_points.select.return_value = eps

        response = client.get(f"{self.path}/applications")

        assert response.status_code == status.HTTP_200_OK

        result = response.json()

        assert result == ["abc", "Blub"]

    @staticmethod
    def mock_distgit_owned_projects(respx_mocker, settings, ownertype):
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
                # Some garbage for the handler to cope with:
                {
                    "description": "Hahahhaha!!!",
                    "fullname": "i-don’t-exist/hahaha",
                    "name": "hahaha",
                    "namespace": "i-don’t-exist",
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

        return route

    @staticmethod
    def mock_distgit_projects(respx_mocker, settings):
        distgit_endpoint = f"{settings.services.distgit_url}/api/0/projects"
        params = {"pattern": "*foobar*"}
        distgit_json_response = {
            "pagination": {
                "pages": 1,
            },
            "projects": [
                {
                    "description": "foobar containers",
                    "fullname": "containers/foobar",
                    "name": "foobar",
                    "namespace": "containers",
                },
                {
                    "description": "foobar rpms",
                    "fullname": "rpms/foobar",
                    "name": "foobar",
                    "namespace": "rpms",
                },
                # Some garbage for the handler to cope with:
                {
                    "description": "Hahahhaha!!!",
                    "fullname": "i-don’t-exist/hahaha",
                    "name": "hahaha",
                    "namespace": "i-don’t-exist",
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

        return route

    @pytest.mark.parametrize("testcase", ("user", "group", "user-group", "name", "nothing"))
    async def test_get_artifacts(self, client, respx_mocker, testcase):
        settings = get_settings()
        settings.services.distgit_url = "http://distgit.test"

        routes = {}
        query_params = {}

        if "user" in testcase:
            routes["user"] = self.mock_distgit_owned_projects(respx_mocker, settings, "user")
            query_params["users"] = ["dudemcpants"]

        if "group" in testcase:
            routes["group"] = self.mock_distgit_owned_projects(respx_mocker, settings, "group")
            query_params["groups"] = ["dudegroup"]

        if "name" in testcase:
            routes["name"] = self.mock_distgit_projects(respx_mocker, settings)
            query_params["names"] = ["*foobar*"]

        response = client.get(f"{self.path}/artifacts", params=query_params)
        result = response.json()

        for what in ("user", "group", "name"):
            if what in testcase:
                assert routes[what].called

        if "user" in testcase or "group" in testcase:
            assert {"name": "pants", "type": "containers"} in result
            assert {"name": "trousers", "type": "rpms"} in result

        if "name" in testcase:
            assert {"name": "foobar", "type": "containers"} in result
            assert {"name": "foobar", "type": "rpms"} in result

        assert result == sorted(result, key=lambda item: (item["type"], item["name"]))

    def test_liveness(self, client):
        response = client.get(f"{self.path}/healthz/live")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"detail": "OK"}

    @pytest.mark.alembic_table_deleted
    async def test_readiness_not_setup(self, client, db_async_session):
        await db_async_session.execute(text("DROP TABLE IF EXISTS alembic_version"))
        await db_async_session.flush()
        response = client.get(f"{self.path}/healthz/ready")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Can't connect to the database" in response.json()["detail"]

    async def test_readiness(self, client, db_manager, db_model_initialized):
        response = client.get(f"{self.path}/healthz/ready")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"detail": "OK"}

    async def test_readiness_needs_upgrade(self, client, db_async_session):
        await db_async_session.execute(text("UPDATE alembic_version SET version_num='foobar'"))
        await db_async_session.flush()
        response = client.get(f"{self.path}/healthz/ready")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json()["detail"] == "Database schema needs to be upgraded"

    async def test_readiness_not_stamped(self, client, db_async_session):
        await db_async_session.execute(text("DELETE FROM alembic_version"))
        await db_async_session.flush()
        response = client.get(f"{self.path}/healthz/ready")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json()["detail"] == "Can't connect to the database"

    async def test_readiness_exception(self, client, db_manager):
        db_manager.get_status = mock.AsyncMock(side_effect=ValueError("dummy"))
        response = client.get(f"{self.path}/healthz/ready")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json()["detail"] == "Can't get the database status: dummy"
