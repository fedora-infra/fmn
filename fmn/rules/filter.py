# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from fnmatch import fnmatch

from fedora_messaging import message

from .requester import Requester


class Filter:
    name: str

    def __init__(self, requester: Requester, params, username):
        self._requester = requester
        self.params = params
        self.username = username

    def matches(self, message: message.Message):
        raise NotImplementedError


class Applications(Filter):
    name = "applications"

    def __init__(self, requester: Requester, params, username):
        if params:
            params = [app_name.lower() for app_name in params]
        super().__init__(requester=requester, params=params, username=username)

    def matches(self, message):
        if not self.params:
            return True
        return message.app_name.lower() in self.params


class Severities(Filter):
    name = "severities"
    default = (message.INFO, message.WARNING, message.ERROR)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._severities = [getattr(message, level.upper()) for level in (self.params or [])]
        if not self._severities:
            self._severities = self.default

    def matches(self, message):
        return message.severity in self._severities


class MyActions(Filter):
    name = "my_actions"

    def matches(self, message):
        if not self.params and self.username == message.agent_name:
            return False
        return True


class Topic(Filter):
    name = "topic"

    def matches(self, message):
        if not self.params:
            return True
        return fnmatch(message.topic, self.params)
