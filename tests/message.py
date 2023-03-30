# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from fedora_messaging import message


class Message(message.Message):
    @property
    def summary(self):
        return self.body.get("summary", f"Message on {self.topic}")

    def __str__(self):
        return self.body.get("content", f"Body of message on {self.topic}")

    @property
    def app_name(self):
        return self.body.get("app")

    @property
    def url(self):
        return self.body.get("url")

    @property
    def usernames(self):
        return self.body.get("usernames", [])

    @property
    def agent_name(self):
        return self.body.get("agent_name")

    @property
    def packages(self):
        return self.body.get("packages", [])

    @property
    def containers(self):
        return self.body.get("containers", [])

    @property
    def modules(self):
        return self.body.get("modules", [])

    @property
    def flatpaks(self):
        return self.body.get("flatpaks", [])
