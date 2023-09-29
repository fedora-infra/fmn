# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from fmn.rules.notification import EmailNotificationContent, IRCNotificationContent


def test_compare_other():
    content = EmailNotificationContent(headers={"To": "dummy", "Subject": "dummy"}, body="dummy")
    other = IRCNotificationContent(to="dummy", message="dummy")
    assert content != other
