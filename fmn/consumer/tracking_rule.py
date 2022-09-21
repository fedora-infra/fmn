from fedora_messaging.message import Message

from fmn.database.model import Rule as RuleRecord

from .requester import Requester


class TrackingRule:

    # This should be the name of the Tracking rule in the Database
    name: str | None = None

    def __init__(self, requester: Requester, params):
        self._requester = requester
        self._params = params

    @classmethod
    def from_rule_record(cls, rule: RuleRecord, requester: Requester):  # noqa
        tracking_rule = rule.tracking_rule
        for subclass in cls.__subclasses__():
            if subclass.name == tracking_rule.name:
                return subclass(requester, tracking_rule.params)
        raise ValueError(f"Unknown tracking rule: {tracking_rule.name}")

    def matches(self, message: Message):
        raise NotImplementedError  # pragma: no cover

    def prime_cache(self):
        raise NotImplementedError  # pragma: no cover


class ArtifactsOwned(TrackingRule):
    name = "artifacts-owned"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = self._params["username"]

    def matches(self, message):
        for package in message.packages:
            if self.username in self._requester.get_package_owners(package):
                return True
        for container in message.containers:
            if self.username in self._requester.get_container_owners(container):
                return True
        for module in message.modules:
            if self.username in self._requester.get_module_owners(module):
                return True
        for flatpak in message.flatpaks:
            if self.username in self._requester.get_flatpak_owners(flatpak):
                return True
        return False

    def prime_cache(self, cache):
        cache["packages"].update(
            self._requester.get_owned_by_user(artifact_type="package", username=self.username)
        )
        cache["containers"].update(
            self._requester.get_owned_by_user(artifact_type="container", username=self.username)
        )
        cache["modules"].update(
            self._requester.get_owned_by_user(artifact_type="module", username=self.username)
        )
        cache["flatpaks"].update(
            self._requester.get_owned_by_user(artifact_type="flatpak", username=self.username)
        )


class ArtifactsGroupOwned(TrackingRule):
    name = "artifacts-group-owned"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = self._params["username"]

    def _get_groups(self):
        groups = self._params["groups"]
        # If no groups were set, then match for all groups
        return set(groups if groups else self._requester.get_user_groups(self.username))

    def matches(self, message):
        groups = self._get_groups()
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

    def prime_cache(self, cache):
        groups = self._get_groups()
        for group in groups:
            cache["packages"].update(
                self._requester.get_owned_by_group(artifact_type="package", group=group)
            )
            cache["containers"].update(
                self._requester.get_owned_by_group(artifact_type="container", group=group)
            )
            cache["modules"].update(
                self._requester.get_owned_by_group(artifact_type="module", group=group)
            )
            cache["flatpaks"].update(
                self._requester.get_owned_by_group(artifact_type="flatpak", group=group)
            )


class ArtifactsFollowed(TrackingRule):
    name = "artifacts-followed"
    artifact_types = {
        # message attribute : artifact type in FMN
        "packages": "package",
        "containers": "container",
        "modules": "module",
        "flatpaks": "flatpak",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.followed = {
            msg_attr: {
                a["name"] for a in self._params if a["type"] == artifact_type or a["type"] == "all"
            }
            for msg_attr, artifact_type in self.artifact_types.items()
        }
        # → packages: {"pkg1", "pkg2", "pkg3"}

    def matches(self, message):
        for msg_attr, followed in self.followed.items():
            if not followed:
                continue
            if set(followed).intersection(set(getattr(message, msg_attr))):
                return True
        return False

    def prime_cache(self, cache):
        for msg_attr, followed in self.followed.items():
            if not followed:
                continue
            cache[msg_attr].update(set(followed))


class RelatedEvents(TrackingRule):
    name = "related-events"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = self._params["username"]

    def matches(self, message):
        return self.username in message.usernames

    def prime_cache(self, cache):
        cache["usernames"].add(self.username)


class UsersFollowed(TrackingRule):
    name = "users-followed"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.followed = self._params["username"]

    def matches(self, message):
        return message.agent_name in self.followed

    def prime_cache(self, cache):
        cache["agent_name"].update(self.followed)
