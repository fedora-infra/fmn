# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from importlib import metadata
from unittest import mock

import httpx
import pytest
from fastapi import status
from httpx import Response
from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound

from fmn.api import api_models, auth
from fmn.core.constants import DEFAULT_MATRIX_DOMAIN
from fmn.database.model import Generated, Rule, User
from fmn.messages.rule import RuleCreateV1, RuleDeleteV1, RuleUpdateV1

from .base import BaseTestAPIV1Handler

PYDANTIC_VER = ".".join(metadata.version("pydantic").split(".")[:2])


@pytest.fixture
def publish(mocker):
    return mocker.patch(
        "fmn.api.handlers.users.publish", side_effect=lambda message: message.validate()
    )


class TestUserHandler(BaseTestAPIV1Handler):
    handler_prefix = "/users"

    @pytest.mark.parametrize("testcase", ("search", "logged-in", "logged-out"))
    def test_get_users(self, testcase, fasjson_user, respx_mocker, fasjson_url, client):
        params = {}
        if "search" in testcase:
            params["search"] = search_term = fasjson_user["username"][:3]
            respx_mocker.get(f"{fasjson_url}/v1/search/users/?username={search_term}").mock(
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

    def test_post_me(self, db_user, api_identity, client):
        response = client.get(f"{self.path}/me")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["id"] == db_user.id
        assert result["name"] == db_user.name
        assert result["is_admin"] is False

    async def test_post_me_new_user(self, api_identity, db_async_session, client):
        async def count_users():
            return (await db_async_session.execute(select(func.count(User.id)))).scalar_one()

        assert (await count_users()) == 0
        response = client.get(f"{self.path}/me")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["id"] == 1
        assert result["name"] == api_identity.name
        assert result["is_admin"] is False
        assert (await count_users()) == 1

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

    def test_get_user_destinations_other_format(
        self, fasjson_user_data, respx_mocker, fasjson_url, client
    ):
        fasjson_user_data["emails"] = ["testuser+extension@example.com"]
        fasjson_user_data["ircnicks"] = [
            "irc:///testuser",
            "irc:/testuser",
            "irc:testuser",
            "irc://example.com/testuser",
            "matrix:/testuser",
            "matrix:///testuser",
            "matrix://example.com/testuser",
            "testuser",
        ]
        expected = [
            {"protocol": "email", "address": "testuser+extension@example.com"},
            {"protocol": "irc", "address": "testuser"},
            {"protocol": "irc", "address": "testuser"},
            {"protocol": "irc", "address": "testuser"},
            {"protocol": "irc", "address": "testuser"},
            {"protocol": "matrix", "address": f"@testuser:{DEFAULT_MATRIX_DOMAIN}"},
            {"protocol": "matrix", "address": f"@testuser:{DEFAULT_MATRIX_DOMAIN}"},
            {"protocol": "matrix", "address": "@testuser:example.com"},
            {"protocol": "irc", "address": "testuser"},
        ]
        respx_mocker.get(f"{fasjson_url}/v1/users/{fasjson_user_data['username']}/").mock(
            return_value=httpx.Response(status.HTTP_200_OK, json={"result": fasjson_user_data})
        )
        response = client.get(f"{self.path}/{fasjson_user_data['username']}/destinations")

        assert response.status_code == status.HTTP_200_OK
        destinations = response.json()
        assert destinations == expected

    @pytest.mark.parametrize("value", (None, []))
    def test_get_user_destinations_no_ircnicks(
        self, fasjson_url, fasjson_user_data, respx_mocker, client, value
    ):
        fasjson_user_data["ircnicks"] = value
        respx_mocker.get(f"{fasjson_url}/v1/users/{fasjson_user_data['username']}/").mock(
            return_value=httpx.Response(status.HTTP_200_OK, json={"result": fasjson_user_data})
        )
        response = client.get(f"{self.path}/{fasjson_user_data['username']}/destinations")

        assert response.status_code == status.HTTP_200_OK

        destinations = response.json()
        assert isinstance(destinations, list)
        irc_destinations = [d for d in destinations if d["protocol"] == "irc"]
        assert len(irc_destinations) == 0

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
            assert result["disabled"] == db_rule.disabled
            assert result["tracking_rule"]["name"] == db_rule.tracking_rule.name
            assert result["tracking_rule"]["params"] == db_rule.tracking_rule.params
        elif testcase == "wrong-user":
            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert isinstance(response.json()["detail"], str)

    @pytest.mark.parametrize("count", (0, 3))
    async def test_get_user_rules_generated(
        self, client, api_identity, db_rule, db_async_session, count
    ):
        """Verify the data about generated notifications in get_user_rules()."""

        for _i in range(count):
            db_async_session.add(Generated(rule=db_rule, count=1))
        await db_async_session.flush()

        response = client.get(f"{self.path}/{api_identity.name}/rules")

        assert response.status_code == status.HTTP_200_OK
        results = response.json()
        assert len(results) == 1
        result = results[0]
        assert "generated_last_week" in result
        assert result["generated_last_week"] == count

    @pytest.mark.parametrize("testcase", ("happy-path", "wrong-user", "no-rule"))
    def test_get_user_rule(self, testcase, client, api_identity, db_rule):
        username = api_identity.name
        if testcase == "wrong-user":
            username = f"not-really-{username}"
        if testcase == "no-rule":
            rule_id = 4242
        else:
            rule_id = db_rule.id

        response = client.get(f"{self.path}/{username}/rules/{rule_id}")

        if testcase == "happy-path":
            assert response.status_code == status.HTTP_200_OK

            result = response.json()
            assert result["name"] == db_rule.name
            assert result["disabled"] == db_rule.disabled
            assert result["tracking_rule"]["name"] == db_rule.tracking_rule.name
            assert result["tracking_rule"]["params"] == db_rule.tracking_rule.params
        elif testcase == "wrong-user":
            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert isinstance(response.json()["detail"], str)
        elif testcase == "no-rule":
            assert response.status_code == status.HTTP_404_NOT_FOUND
            assert isinstance(response.json()["detail"], str)

    @pytest.mark.parametrize(
        "testcase",
        (
            "success",
            "success-delete-generation-rule",
            "success-delete-destination",
            "success-delete-filter",
            "success-modify-filter",
            "success-disable",
            "wrong-user",
        ),
    )
    async def test_edit_user_rule(self, publish, testcase, client, api_identity, db_rule):
        username = api_identity.name
        if testcase == "wrong-user":
            username = f"not-really-{username}"

        edited_rule = api_models.Rule.model_validate(db_rule)
        edited_rule.tracking_rule.name = "artifacts-group-owned"
        if "delete-generation-rule" in testcase:
            del edited_rule.generation_rules[-1]
        elif "delete-destination" in testcase:
            del edited_rule.generation_rules[-1].destinations[-1]
        elif "delete-filter" in testcase:
            del edited_rule.generation_rules[-1].filters.applications
        elif "modify-filter" in testcase:
            edited_rule.generation_rules[-1].filters.applications = ["koji"]
        elif "disable" in testcase:
            edited_rule.disabled = True
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
                "rule": edited_rule.model_dump(),
                "user": api_models.User.model_validate(db_rule.user).model_dump(),
            }
        )
        if testcase == "success":
            success_message.body["rule"]["generation_rules"][-1]["id"] = len(
                success_message.body["rule"]["generation_rules"]
            )
        if "delete-filter" in testcase:
            success_message.body["rule"]["generation_rules"][-1]["filters"]["applications"] = []

        response = client.put(
            f"{self.path}/{username}/rules/{db_rule.id}",
            json=edited_rule.model_dump(exclude_unset=True),
        )

        if "success" in testcase:
            publish.assert_awaited_once_with(success_message)

            assert response.status_code == status.HTTP_200_OK

            result = response.json()
            assert result["id"] == edited_rule.id
            assert result["name"] == db_rule.name
            assert result["tracking_rule"]["name"] == "artifacts-group-owned"
            assert result["tracking_rule"]["params"] == db_rule.tracking_rule.params
            if "disable" in testcase:
                assert result["disabled"] is True
        else:
            publish.assert_not_called()
            if testcase == "wrong-user":
                assert response.status_code == status.HTTP_403_FORBIDDEN
                assert isinstance(response.json()["detail"], str)

    @pytest.mark.parametrize("testcase", ("happy-path", "wrong-user"))
    async def test_delete_user_rule(
        self, publish, testcase, client, api_identity, db_rule, db_async_session
    ):
        username = api_identity.name
        if testcase == "wrong-user":
            username = f"not-really-{username}"

        message = RuleDeleteV1(
            body={
                "rule": api_models.Rule.model_validate(db_rule).model_dump(),
                "user": api_models.User.model_validate(db_rule.user).model_dump(),
            }
        )

        response = client.delete(f"{self.path}/{username}/rules/{db_rule.id}")

        if testcase == "happy-path":
            publish.assert_awaited_once_with(message)
            assert response.status_code == status.HTTP_200_OK
            with pytest.raises(NoResultFound):
                await Rule.get_one(session=db_async_session, id=db_rule.id)
        else:
            publish.assert_not_called()
            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert isinstance(response.json()["detail"], str)

    @pytest.mark.parametrize("testcase", ("success", "wrong-user"))
    async def test_create_user_rule(
        self, publish, testcase, client, api_identity, db_user, db_rule
    ):
        username = api_identity.name
        if testcase == "wrong-user":
            username = f"not-really-{username}"

        user = api_models.User.model_validate(db_rule.user)
        created_rule = api_models.NewRule(
            **{
                "name": "daotherrule",
                "tracking_rule": {"name": "users-followed", "params": ["dummy"]},
                "generation_rules": [
                    {
                        "destinations": [{"protocol": "irc", "address": "dummynick"}],
                        "filters": {},
                    },
                ],
            }
        )

        message = RuleCreateV1(body={"rule": created_rule.model_dump(), "user": user.model_dump()})
        # Assume the rule will be created with id = 2 (because db_rule already exists)
        message.body["rule"]["id"] = 2
        # In the message the rule will have the user dict in it
        message.body["rule"]["user"] = user.model_dump()
        message.body["rule"]["generated_last_week"] = 0
        message.body["rule"]["generation_rules"][0]["id"] = 3

        response = client.post(
            f"{self.path}/{username}/rules", json=created_rule.model_dump(exclude_unset=True)
        )

        if "success" in testcase:
            publish.assert_awaited_once_with(message)
            assert response.status_code == status.HTTP_200_OK

            result = response.json()
            assert result["id"] not in (None, db_rule.id)
            assert result["name"] == "daotherrule"
            assert result["tracking_rule"]["name"] == "users-followed"
            assert result["generation_rules"] == [
                {
                    "id": 3,
                    "destinations": [{"protocol": "irc", "address": "dummynick"}],
                    "filters": {
                        "applications": [],
                        "severities": [],
                        "topic": None,
                        "my_actions": False,
                    },
                },
            ]
        else:
            publish.assert_not_called()
            if testcase == "wrong-user":
                assert response.status_code == status.HTTP_403_FORBIDDEN
                assert isinstance(response.json()["detail"], str)

    async def test_create_user_rule_bad_matrix_dest(self, client, api_identity, db_rule, caplog):
        created_rule = {
            "name": "wrongrule",
            "tracking_rule": {"name": "users-followed", "params": ["dummy"]},
            "generation_rules": [
                {
                    "destinations": [{"protocol": "matrix", "address": "dummynick"}],
                    "filters": {},
                },
            ],
        }

        response = client.post(f"{self.path}/{api_identity.name}/rules", json=created_rule)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        expected_message = (
            "The Matrix address 'dummynick' should be in the form @username:server.tld"
        )
        assert response.json()["detail"] == [
            {
                "loc": ["body", "generation_rules", 0, "destinations", 0, "address"],
                "msg": f"Value error, {expected_message}",
                "type": "value_error",
                "input": "dummynick",
                "ctx": {"error": {}},
                "url": f"https://errors.pydantic.dev/{PYDANTIC_VER}/v/value_error",
            }
        ]
        assert caplog.messages == [expected_message]

    async def test_create_user_rule_bad_email_dest(self, client, api_identity, db_rule, caplog):
        created_rule = {
            "name": "wrongrule",
            "tracking_rule": {"name": "users-followed", "params": ["dummy"]},
            "generation_rules": [
                {
                    "destinations": [{"protocol": "email", "address": "wrongvalue"}],
                    "filters": {},
                },
            ],
        }

        response = client.post(f"{self.path}/{api_identity.name}/rules", json=created_rule)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        expected_message = "The email address 'wrongvalue' does not look right"
        assert response.json()["detail"] == [
            {
                "loc": ["body", "generation_rules", 0, "destinations", 0, "address"],
                "msg": f"Value error, {expected_message}",
                "type": "value_error",
                "ctx": {"error": {}},
                "input": "wrongvalue",
                "url": f"https://errors.pydantic.dev/{PYDANTIC_VER}/v/value_error",
            }
        ]
        assert caplog.messages == [expected_message]

    async def test_create_user_rule_related_events(self, client, api_identity, db_rule, caplog):
        created_rule = {
            "name": None,
            "tracking_rule": {"name": "related-events"},
            "generation_rules": [
                {
                    "destinations": [{"protocol": "matrix", "address": "@dummy:example.com"}],
                    "filters": {},
                },
            ],
        }

        response = client.post(f"{self.path}/{api_identity.name}/rules", json=created_rule)
        assert response.status_code == status.HTTP_200_OK
        rule = response.json()
        assert rule["tracking_rule"]["name"] == "related-events"
        assert rule["tracking_rule"]["params"] is None
