import logging
from typing import TYPE_CHECKING

from fmn.core.constants import ArtifactType

from .requester import Requester

if TYPE_CHECKING:
    from fedora_messaging.message import Message


log = logging.getLogger(__name__)


class TrackingRule:

    # This should be the name of the Tracking rule in the Database
    name: str | None = None

    def __init__(self, requester: Requester, params, owner):
        self._requester = requester
        self._params = params
        self._owner = owner

    def matches(self, message: "Message"):
        raise NotImplementedError  # pragma: no cover

    def prime_cache(self, cache):
        raise NotImplementedError  # pragma: no cover


class ArtifactsOwned(TrackingRule):
    name = "artifacts-owned"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usernames = set(self._params)

    def matches(self, message):
        for package in message.packages:
            if self.usernames & set(self._requester.get_package_owners(package)):
                return True
        for container in message.containers:
            if self.usernames & set(self._requester.get_container_owners(container)):
                return True
        for module in message.modules:
            if self.usernames & set(self._requester.get_module_owners(module)):
                return True
        for flatpak in message.flatpaks:
            if self.usernames & set(self._requester.get_flatpak_owners(flatpak)):
                return True
        return False

    def prime_cache(self, cache):
        for username in self.usernames:
            cache["packages"].update(
                self._requester.get_owned_by_user(artifact_type="packages", name=username)
            )
            cache["containers"].update(
                self._requester.get_owned_by_user(artifact_type="containers", name=username)
            )
            cache["modules"].update(
                self._requester.get_owned_by_user(artifact_type="modules", name=username)
            )
            cache["flatpaks"].update(
                self._requester.get_owned_by_user(artifact_type="flatpaks", name=username)
            )


class ArtifactsGroupOwned(TrackingRule):
    name = "artifacts-group-owned"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.groups = set(self._params)

    def matches(self, message):
        for package in message.packages:
            if self.groups & set(self._requester.get_package_group_owners(package)):
                return True
        for container in message.containers:
            if self.groups & set(self._requester.get_container_group_owners(container)):
                return True
        for module in message.modules:
            if self.groups & set(self._requester.get_module_group_owners(module)):
                return True
        for flatpak in message.flatpaks:
            if self.groups & set(self._requester.get_flatpak_group_owners(flatpak)):
                return True
        return False

    def prime_cache(self, cache):
        for group in self.groups:
            cache["packages"].update(
                self._requester.get_owned_by_group(artifact_type="packages", name=group)
            )
            cache["containers"].update(
                self._requester.get_owned_by_group(artifact_type="containers", name=group)
            )
            cache["modules"].update(
                self._requester.get_owned_by_group(artifact_type="modules", name=group)
            )
            cache["flatpaks"].update(
                self._requester.get_owned_by_group(artifact_type="flatpaks", name=group)
            )


class ArtifactsFollowed(TrackingRule):
    name = "artifacts-followed"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.followed = {
            atype.name: {p["name"] for p in self._params if p["type"] == atype.value}
            for atype in ArtifactType
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
            cache[msg_attr].update(followed)


class RelatedEvents(TrackingRule):
    name = "related-events"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def matches(self, message):
        return self._owner in message.usernames

    def prime_cache(self, cache):
        cache["usernames"].add(self._owner)


class UsersFollowed(TrackingRule):
    name = "users-followed"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.followed = set(self._params)

    def matches(self, message):
        return message.agent_name in self.followed

    def prime_cache(self, cache):
        cache["agent_name"].update(self.followed)
