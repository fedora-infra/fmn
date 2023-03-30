# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from fmn.messages.rule import RuleCreateV1


def test_messages_base():
    message = RuleCreateV1({"rule": {}, "user": {}})
    assert message.app_name == "FMN"
    assert message.app_icon == "https://apps.fedoraproject.org/img/icons/fedmsg.png"
