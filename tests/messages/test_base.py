# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import pytest
from fedora_messaging.message import ValidationError

from fmn.messages.rule import RuleCreateV1


def test_messages_base():
    message = RuleCreateV1({"rule": {}, "user": {}})
    assert message.app_name == "FMN"
    assert message.app_icon == "https://apps.fedoraproject.org/img/icons/fedmsg.png"


def test_messages_rule_no_name():
    message = RuleCreateV1({"rule": {"name": None}, "user": {}})
    try:
        message.validate()
    except ValidationError as e:
        pytest.fail(e)
