from fedora_messaging.message import Message

from .requester import Requester


class TrackingRule:

    # This should be the name of the Tracking rule in the Database
    name: str | None = None

    def __init__(self, requester: Requester, **params):
        self._requester = requester
        self._params = params

    @classmethod
    def from_rule(cls, rule: "RuleRecord", requester: Requester):  # noqa
        for subclass in cls.__subclasses__:
            if not subclass.name:
                continue
            if subclass.name == rule.tracking_rule:
                return subclass(requester, rule.tracking_rule_params)

    def matches(self, message: Message):
        raise NotImplementedError


class ArtifactsOwned(TrackingRule):
    name = "artifacts-owned"

    def matches(self, message):
        username = self._params["username"]
        for package in message.packages:
            if username in self._requester.get_package_owners(package):
                return True
        for container in message.containers:
            if username in self._requester.get_container_owners(container):
                return True
        for module in message.modules:
            if username in self._requester.get_module_owners(module):
                return True
        for flatpak in message.flatpaks:
            if username in self._requester.get_flatpak_owners(flatpak):
                return True
        return False


class ArtifactsGroupOwned(TrackingRule):
    name = "artifacts-group-owned"

    def matches(self, message):
        username = self._params["username"]
        groups = self._params["groups"]
        # If no groups were set, then match for all groups
        groups = set(groups if groups else self._requester.get_user_groups(username))
        for package in message.packages:
            if groups.intersection(set(self._requester.get_package_group_owners(package))):
                return True
        for container in message.containers:
            if groups.intersection(set(self._requester.get_container_group_owners(container))):
                return True
        for module in message.modules:
            if groups.intersection(set(self._requester.get_module_group_owners(module))):
                return True
        for flatpak in message.flatpaks:
            if groups.intersection(set(self._requester.get_flatpak_group_owners(flatpak))):
                return True
        return False


class ArtifactsFollowed(TrackingRule):
    name = "artifacts-followed"
    artifact_types = {
        # message attribute : artifact type in FMN
        "packages": "package",
        "containers": "container",
        "modules": "module",
        "flatpaks": "flatpak",
    }

    def __init__(self, args, **kwargs):
        super().__init__(*args, **kwargs)
        self._artifacts = self._params["artifacts"]
        self.followed = {
            msg_attr: set(
                [
                    a["name"]
                    for a in self._artifacts
                    if a["type"] == artifact_type or a["type"] == "all"
                ]
            )
            for msg_attr, artifact_type in self.artifact_types.items()
        }

    def matches(self, message):
        for artifact_type, followed in self.followed.items():
            if not followed:
                continue
            if followed.intersection(set(getattr(message, artifact_type))):
                return True
        return False


class RelatedEvents(TrackingRule):
    name = "related-events"

    def matches(self, message):
        username = self._params["username"]
        return username in message.usernames


class UsersFollowed(TrackingRule):
    name = "users-followed"

    def matches(self, message):
        followed = self._params["usernames"]
        return message.author in followed
