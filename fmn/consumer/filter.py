from fnmatch import fnmatch

from fedora_messaging import message

from fmn.database.model import Filter as FilterRecord

from .requester import Requester


class Filter:
    name: str

    def __init__(self, requester, params):
        self._requester = requester
        self.params = params

    @classmethod
    def from_record(cls, record: FilterRecord, requester: Requester):
        subclasses = {s.name: s for s in cls.__subclasses__()}
        return subclasses[record.name](
            params=record.params,
            requester=requester,
        )

    def matches(self, message: message.Message):
        raise NotImplementedError  # pragma: no cover


class ApplicationsFilter(Filter):
    name = "applications"

    def matches(self, message):
        return message.app_name in self.params


class SeveritiesFilter(Filter):
    name = "severities"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._severities = [getattr(message, level.upper()) for level in self.params]

    def matches(self, message):
        return message.severity in self._severities


class NotMyActionsFilter(Filter):
    name = "not_my_actions"

    def matches(self, message):
        return self.params != message.agent_name


class TopicFilter(Filter):
    name = "topic"

    def matches(self, message):
        return fnmatch(message.topic, self.params)
