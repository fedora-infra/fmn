# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from fmn.sender.config import get_handler
from fmn.sender.email import EmailHandler


def test_get_handler():
    handler = get_handler({"handler": {"class": "fmn.sender.email:EmailHandler"}})
    assert isinstance(handler, EmailHandler)
