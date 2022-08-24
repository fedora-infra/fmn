from fnmatch import fnmatch

from fedora_messaging import message

from .destination import Destination
from .requester import Requester


class Filter:
    name: str
    username: str
    destinations: list[Destination]

    def __init__(self, username, requester, params):
        self.username = username
        self._requester = requester
        self.params = params

    @classmethod
    def from_rule(cls, rule: RuleRecord, requester: Requester):  # noqa
        subclasses = {s.name: s for s in cls.__subclasses__}
        filters = []
        for filter_name in rule.filters:
            f = subclasses[filter_name](
                username=rule.username, requester=requester, params=rule.filter_params
            )
            f.destinations = Destination.from_rule(rule)
            filters.append(f)
        return filters

    def matches(self, message: message.Message):
        raise NotImplementedError


class ApplicationsFilter(Filter):
    name = "applications"

    def matches(self, message):
        return message.app_name in self.params["applications"]


class SeveritiesFilter(Filter):
    name = "severities"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._severities = [getattr(message, level.upper()) for level in self.params["severities"]]

    def matches(self, message):
        return message.severity in self._severities


class NotMyActionsFilter(Filter):
    name = "not_my_actions"

    def matches(self, message):
        return self.username != message.author


class TopicFilter(Filter):
    name = "topic"

    def matches(self, message):
        return fnmatch(message.topic, self.params["topic"])
