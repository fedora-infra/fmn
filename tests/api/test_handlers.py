import re
from unittest import mock

import pytest
from fastapi import status
from fedora_messaging.testing import mock_sends
from httpx import Response
from sqlalchemy.exc import NoResultFound

from fmn.api import api_models, auth
from fmn.api.handlers.utils import get_last_messages
from fmn.core.config import get_settings
from fmn.database.model import Rule
from fmn.messages.rule import RuleCreateV1, RuleDeleteV1, RuleUpdateV1


@pytest.mark.usefixtures("mocked_fasjson", "mocked_fasjson_client")
class BaseTestHandler:
    api_prefix = None
    handler_prefix = None

    @property
    def path(self):
        return (self.api_prefix or "") + (self.handler_prefix or "")


class BaseTestAPIV1Handler(BaseTestHandler):
    api_prefix = "/api/v1"


class TestUserHandler(BaseTestAPIV1Handler):
    handler_prefix = "/users"

    @pytest.mark.parametrize("testcase", ("search", "logged-in", "logged-out"))
    def test_get_users(self, testcase, fasjson_user, async_respx_mocker, fasjson_url, client):
        params = {}
        if "search" in testcase:
            params["search"] = search_term = fasjson_user["username"][:3]
            async_respx_mocker.get(f"{fasjson_url}/v1/search/users/?username={search_term}").mock(
                side_effect=[
                    Response(
                        status.HTTP_200_OK,
                        json={
                            "result": [fasjson_user],
                            "page": {"page_number": 1, "total_pages": 1},
                        },
                    )
                ]
            )
            expected_result = [fasjson_user["username"]]
        elif "logged" in testcase:
            fake_identity = mock.Mock()
            if "logged-in" in testcase:
                fake_identity.name = "logged-in-user"
                expected_result = [fake_identity.name]
            else:  # logged-out
                fake_identity.name = None
                expected_result = []
            client.app.dependency_overrides[auth.get_identity_optional] = lambda: fake_identity

        response = client.get(f"{self.path}", params=params)
        assert response.status_code == status.HTTP_200_OK

        assert response.json() == expected_result

    def test_get_user_info(self, fasjson_user, client):
        """Test that get_user_info() dispatches to FASJSON."""
        username = fasjson_user["username"]
        response = client.get(f"{self.path}/{username}/info")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == fasjson_user

    def test_get_user(self, fasjson_user, db_user, client):
        username = fasjson_user["username"]
        response = client.get(f"{self.path}/{username}")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["id"] == db_user.id
        assert result["name"] == db_user.name

    def test_get_user_groups(self, fasjson_user, fasjson_groups, client):
        username = fasjson_user["username"]

        response = client.get(f"{self.path}/{username}/groups")

        assert response.status_code == status.HTTP_200_OK

        groups = response.json()
        assert sorted(groups) == sorted(item["groupname"] for item in fasjson_groups)

    def test_get_user_destinations(self, fasjson_user, client):
        response = client.get(f"{self.path}/{fasjson_user['username']}/destinations")

        assert response.status_code == status.HTTP_200_OK

        destinations = response.json()
        assert isinstance(destinations, list)
        assert all(isinstance(item, dict) for item in destinations)
        assert all("protocol" in item for item in destinations)
        assert all("address" in item for item in destinations)

    @pytest.mark.parametrize("testcase", ("happy-path", "wrong-user"))
    def test_get_user_rules(self, testcase, client, api_identity, db_rule):
        """Verify the results of get_user_rules()."""
        username = api_identity.name
        if testcase == "wrong-user":
            username = f"not-really-{username}"

        response = client.get(f"{self.path}/{username}/rules")

        if testcase == "happy-path":
            assert response.status_code == status.HTTP_200_OK

            results = response.json()
            assert isinstance(results, list)
            assert len(results) == 1

            result = results[0]
            assert result["name"] == db_rule.name
            assert result["tracking_rule"]["name"] == db_rule.tracking_rule.name
            assert result["tracking_rule"]["params"] == db_rule.tracking_rule.params
        elif testcase == "wrong-user":
            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert isinstance(response.json()["detail"], str)

    @pytest.mark.parametrize("testcase", ("happy-path", "wrong-user"))
    def test_get_user_rule(self, testcase, client, api_identity, db_rule):
        username = api_identity.name
        if testcase == "wrong-user":
            username = f"not-really-{username}"

        response = client.get(f"{self.path}/{username}/rules/{db_rule.id}")

        if testcase == "happy-path":
            assert response.status_code == status.HTTP_200_OK

            result = response.json()
            assert result["name"] == db_rule.name
            assert result["tracking_rule"]["name"] == db_rule.tracking_rule.name
            assert result["tracking_rule"]["params"] == db_rule.tracking_rule.params
        elif testcase == "wrong-user":
            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert isinstance(response.json()["detail"], str)

    @pytest.mark.parametrize(
        "testcase",
        (
            "success",
            "success-delete-generation-rule",
            "success-delete-destination",
            "success-delete-filter",
            "wrong-user",
        ),
    )
    def test_edit_user_rule(self, testcase, client, api_identity, db_rule):
        username = api_identity.name
        if testcase == "wrong-user":
            username = f"not-really-{username}"

        edited_rule = api_models.Rule.from_orm(db_rule)
        edited_rule.tracking_rule.name = "artifacts-group-owned"
        if "delete-generation-rule" in testcase:
            del edited_rule.generation_rules[-1]
        elif "delete-destination" in testcase:
            del edited_rule.generation_rules[-1].destinations[-1]
        elif "delete-filter" in testcase:
            del edited_rule.generation_rules[-1].filters.applications
        elif "modify-filter" in testcase:
            edited_rule.generation_rules[-1].filters.applications = ["koji"]
        else:
            edited_rule.generation_rules.append(
                api_models.GenerationRule(destinations=[], filters=api_models.Filters())
            )
            edited_rule.generation_rules[-1].destinations.append(
                api_models.Destination(protocol="foo", address="bar")
            )
            edited_rule.generation_rules[-1].filters.severities = ["very severe"]

        success_message = RuleUpdateV1(
            body={
                "rule": edited_rule.dict(),
                "user": api_models.User.from_orm(db_rule.user).dict(),
            }
        )
        if "delete-filter" in testcase:
            success_message.body["rule"]["generation_rules"][-1]["filters"]["applications"] = []
        with mock_sends(*([success_message] if "success" in testcase else [])):
            response = client.put(
                f"{self.path}/{username}/rules/{db_rule.id}",
                data=edited_rule.json(exclude_unset=True),
            )

        if "success" in testcase:
            assert response.status_code == status.HTTP_200_OK

            result = response.json()
            assert result["id"] == edited_rule.id
            assert result["name"] == db_rule.name
            assert result["tracking_rule"]["name"] == "artifacts-group-owned"
            assert result["tracking_rule"]["params"] == db_rule.tracking_rule.params
        elif testcase == "wrong-user":
            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert isinstance(response.json()["detail"], str)

    @pytest.mark.parametrize("testcase", ("happy-path", "wrong-user"))
    async def test_delete_user_rule(
        self, testcase, client, api_identity, db_rule, db_async_session
    ):
        username = api_identity.name
        if testcase == "wrong-user":
            username = f"not-really-{username}"

        message = RuleDeleteV1(
            body={
                "rule": api_models.Rule.from_orm(db_rule).dict(),
                "user": api_models.User.from_orm(db_rule.user).dict(),
            }
        )
        with mock_sends(*([message] if testcase == "happy-path" else [])):
            response = client.delete(f"{self.path}/{username}/rules/{db_rule.id}")

        if testcase == "happy-path":
            assert response.status_code == status.HTTP_200_OK
            with pytest.raises(NoResultFound):
                await Rule.async_get(db_async_session, id=db_rule.id)
        else:
            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert isinstance(response.json()["detail"], str)

    @pytest.mark.parametrize("testcase", ("success", "wrong-user"))
    def test_create_user_rule(self, testcase, client, api_identity, db_rule):
        username = api_identity.name
        if testcase == "wrong-user":
            username = f"not-really-{username}"

        created_rule = api_models.Rule(
            **{
                "name": "daotherrule",
                "tracking_rule": {"name": "users-followed", "params": ["dummy"]},
                "generation_rules": [
                    {
                        "destinations": [{"protocol": "irc", "address": "..."}],
                        "filters": {},
                    },
                ],
            }
        )

        message = RuleCreateV1(
            body={
                "rule": created_rule.dict(),
                "user": api_models.User.from_orm(db_rule.user).dict(),
            }
        )
        # Assume the rule will be created with id = 2 (because db_rule already exists)
        message.body["rule"]["id"] = 2
        with mock_sends(*([message] if "success" in testcase else [])):
            response = client.post(
                f"{self.path}/{username}/rules", data=created_rule.json(exclude_unset=True)
            )

        if "success" in testcase:
            assert response.status_code == status.HTTP_200_OK

            result = response.json()
            assert result["id"] not in (None, db_rule.id)
            assert result["name"] == "daotherrule"
            assert result["tracking_rule"]["name"] == "users-followed"
            assert result["generation_rules"] == [
                {
                    "destinations": [{"protocol": "irc", "address": "..."}],
                    "filters": {
                        "applications": [],
                        "severities": [],
                        "topic": None,
                        "my_actions": False,
                    },
                },
            ]
        elif testcase == "wrong-user":
            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert isinstance(response.json()["detail"], str)


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
            "mdapi",
            "noggin",
            "nuancier",
            "pagure",
            "planet",
        ]

    @pytest.mark.parametrize("ownertype", ("user", "group"))
    async def test_get_projects(self, client, mocker, async_respx_mocker, ownertype):
        settings = get_settings()
        settings.services.distgit_url = "http://distgit.test"
        mocker.patch("fmn.api.handlers.utils.get_settings", return_value=settings)

        # async_respx_mocker.route(host="distgit.test").pass_through()

        if ownertype == "user":
            params = {"fork": "false", "short": "true", "page": 1, "owner": "dudemcpants"}
        elif ownertype == "group":
            params = {"fork": "false", "short": "true", "page": 1, "username": "@dudegroup"}

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
                },
                {
                    "description": "trousers rpms",
                    "fullname": "rpms/trousers",
                    "name": "trousers",
                    "namespace": "rpms",
                },
            ],
        }

        route = async_respx_mocker.get(
            f"{settings.services.distgit_url}/api/0/projects", params=params
        ).mock(
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
        await db_async_session.execute("DROP TABLE IF EXISTS alembic_version")
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
        await db_async_session.execute("UPDATE alembic_version SET version_num='foobar'")
        mocker.patch("fmn.api.database.async_session_maker", return_value=db_async_session)
        response = client.get(f"{self.path}/healthz/ready")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json()["detail"] == "Database schema needs to be upgraded"

    async def test_readiness_not_stamped(self, client, db_async_session, mocker):
        await db_async_session.execute("DELETE FROM alembic_version")
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

    def test_preview_basic(
        self, mocker, responses_mocker, client, api_identity, make_mocked_message
    ):
        mocker.patch("fmn.rules.services.fasjson.Client")
        responses_mocker.get(
            "https://apps.fedoraproject.org/datagrepper/v2/search?"
            "page=1&rows_per_page=100&delta=3600",
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

    def test_preview_anonymous(self, mocker, client, api_identity):
        api_identity.name = None
        mocker.patch("fmn.rules.services.fasjson.Client")
        response = client.post(f"{self.path}/rule-preview", json=self._dummy_rule_dict)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_dg_url_fix(self, mocker, responses_mocker):
        settings = get_settings()
        settings.services.datagrepper_url = "http://datagrepper.test"
        mocker.patch("fmn.api.handlers.utils.get_settings", return_value=settings)
        resp = responses_mocker.get(
            re.compile(r"http://datagrepper\.test/v2/search.*"),
            json={
                "raw_messages": [],
                "pages": 0,
            },
        )
        messages = list(get_last_messages(1))
        assert messages == []
        assert resp.call_count == 1

    def test_get_last_messages_pages(self, mocker, responses_mocker, make_mocked_message):
        rsp1 = responses_mocker.get(
            "https://apps.fedoraproject.org/datagrepper/v2/search?"
            "page=1&rows_per_page=100&delta=3600",
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
                "pages": 2,
            },
        )
        rsp2 = responses_mocker.get(
            "https://apps.fedoraproject.org/datagrepper/v2/search?"
            "page=2&rows_per_page=100&delta=3600",
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
                "pages": 2,
            },
        )

        messages = list(get_last_messages(1))

        assert len(messages) == 2
        assert rsp1.call_count == 1
        assert rsp2.call_count == 1
