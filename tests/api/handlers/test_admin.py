# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import pytest
from fastapi import status

from fmn.api import api_models
from fmn.messages.rule import RuleUpdateV1

from .base import BaseTestAPIV1Handler


@pytest.fixture
def publish(mocker):
    return mocker.patch(
        "fmn.api.handlers.admin.publish", side_effect=lambda message: message.validate()
    )


class TestAdmin(BaseTestAPIV1Handler):
    handler_prefix = "/admin"

    def test_admin_rules_forbidden(self, client, api_identity):
        api_identity.admin = False
        response = client.get(f"{self.path}/rules")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("with_disabled", (True, False))
    def test_list_rules(self, with_disabled, client, api_identity, db_rule, db_rule_disabled):
        api_identity.admin = True

        if with_disabled:
            params = {"disabled": True}
        else:
            params = {}

        response = client.get(f"{self.path}/rules", params=params)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        if with_disabled:
            assert len(result) == 1
        else:
            assert len(result) == 2

        assert result[-1] == {
            "id": 2,
            "name": "disabledrule",
            "disabled": True,
            "user": {"id": 2, "name": "dudemcpants", "is_admin": False},
            "tracking_rule": {"name": "users-followed", "params": ["user1", "user2"]},
            "generation_rules": [
                {
                    "id": 3,
                    "destinations": [{"protocol": "email", "address": "dude@mcpants"}],
                    "filters": {
                        "applications": [],
                        "severities": [],
                        "topic": None,
                        "my_actions": False,
                    },
                }
            ],
            "generated_last_week": 0,
        }

    def test_list_rules_username(self, client, api_identity, db_rule, db_rule_disabled):
        api_identity.admin = True

        params = {"username": "dudemcpants"}

        response = client.get(f"{self.path}/rules", params=params)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert len(result) == 1

        assert result[-1] == {
            "id": 2,
            "name": "disabledrule",
            "disabled": True,
            "user": {"id": 2, "name": "dudemcpants", "is_admin": False},
            "tracking_rule": {"name": "users-followed", "params": ["user1", "user2"]},
            "generation_rules": [
                {
                    "id": 3,
                    "destinations": [{"protocol": "email", "address": "dude@mcpants"}],
                    "filters": {
                        "applications": [],
                        "severities": [],
                        "topic": None,
                        "my_actions": False,
                    },
                }
            ],
            "generated_last_week": 0,
        }

    @pytest.mark.parametrize("searchterm", ("u", "dudemc", None))
    def test_get_users(self, searchterm, client, api_identity, db_rule, db_rule_disabled):
        api_identity.admin = True

        if searchterm:
            params = {"search": searchterm}
        else:
            params = {}

        response = client.get(f"{self.path}/users", params=params)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()

        if searchterm == "u":
            assert len(result) == 2
        if searchterm == "dudemc":
            assert len(result) == 1
        if searchterm is None:
            assert len(result) == 2

    def test_reenable_rule(self, publish, client, api_identity, db_rule, db_rule_disabled):
        api_identity.admin = True

        # First check we have one disabled rule
        response = client.get(f"{self.path}/rules", params={"disabled": True})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

        # Next re-enable the rule
        response = client.patch(f"{self.path}/rules/2", json={"disabled": False})
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["name"] == "disabledrule"
        assert result["disabled"] is False

        # Finally check we have no disabled rules anymore
        response = client.get(f"{self.path}/rules", params={"disabled": True})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 0

        edited_rule = api_models.Rule.model_validate(db_rule_disabled)
        edited_rule.disabled = False
        success_message = RuleUpdateV1(
            body={
                "rule": edited_rule.model_dump(),
                "user": api_models.User.model_validate(db_rule_disabled.user).model_dump(),
            }
        )
        publish.assert_awaited_once_with(success_message)

    async def test_disable_rule(self, publish, client, api_identity, db_rule):
        api_identity.admin = True

        # First check we have no disabled rules
        response = client.get(f"{self.path}/rules", params={"disabled": True})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 0

        # Next re-enable the rule
        response = client.patch(f"{self.path}/rules/1", json={"disabled": True})
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["name"] == "darule"
        assert result["disabled"] is True

        # Finally check we have no disabled rules anymore
        response = client.get(f"{self.path}/rules", params={"disabled": True})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

        edited_rule = api_models.Rule.model_validate(db_rule)
        edited_rule.disabled = True
        success_message = RuleUpdateV1(
            body={
                "rule": edited_rule.model_dump(),
                "user": api_models.User.model_validate(db_rule.user).model_dump(),
            }
        )
        publish.assert_awaited_once_with(success_message)

    def test_rule_not_found(self, client, api_identity, db_rule):
        api_identity.admin = True

        response = client.patch(f"{self.path}/rules/233", json={"disabled": True})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_rule_patch_nothing(self, client, api_identity, db_rule):
        api_identity.admin = True

        response = client.get(f"{self.path}/rules")
        assert response.status_code == status.HTTP_200_OK
        rules = response.json()
        assert len(rules) == 1
        rule = rules[0]

        response = client.patch(f"{self.path}/rules/{rule['id']}", json={})
        assert response.status_code == status.HTTP_200_OK
        patched_rule = response.json()
        assert patched_rule == rule
