# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from fedora_messaging import message


class BaseMessage(message.Message):
    @property
    def app_name(self):
        return "FMN"

    @property
    def app_icon(self):
        return "https://apps.fedoraproject.org/img/icons/fedmsg.png"
