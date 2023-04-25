# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import pytest
from jsonschema.exceptions import ValidationError

from fmn.messages.rule import RuleCreateV1


def test_messages_base():
    message = RuleCreateV1({"rule": {"id": 1}, "user": {"name": "dummy"}})
    assert message.app_name == "FMN"
    assert message.app_icon == "https://apps.fedoraproject.org/img/icons/fedmsg.png"
    try:
        message.validate()
    except ValidationError as e:
        pytest.fail(e)


def test_messages_rule_no_name():
    message = RuleCreateV1({"rule": {"id": 1, "name": None}, "user": {"name": "dummy"}})
    try:
        message.validate()
    except ValidationError as e:
        pytest.fail(e)


@pytest.mark.parametrize(
    "body", [{"rule": {}, "user": {"name": "dummy"}}, {"rule": {"id": 1}, "user": {}}]
)
def test_messages_rule_missing_values(body):
    message = RuleCreateV1(body)
    with pytest.raises(ValidationError):
        message.validate()
