from fnmatch import fnmatch

from fedora_messaging import message

from .requester import Requester


class Filter:
    name: str

    def __init__(self, requester: Requester, params):
        self._requester = requester
        self.params = params

    def matches(self, message: message.Message):
        raise NotImplementedError  # pragma: no cover


class Applications(Filter):
    name = "applications"

    def matches(self, message):
        return message.app_name in self.params


class Severities(Filter):
    name = "severities"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._severities = [getattr(message, level.upper()) for level in self.params]

    def matches(self, message):
        return message.severity in self._severities


class NotMyActions(Filter):
    name = "not_my_actions"

    def matches(self, message):
        return self.params != message.agent_name


class Topic(Filter):
    name = "topic"

    def matches(self, message):
        return fnmatch(message.topic, self.params)
