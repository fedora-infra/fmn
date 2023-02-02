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

    async def matches(self, message: "Message"):
        raise NotImplementedError  # pragma: no cover

    async def prime_cache(self, cache):
        raise NotImplementedError  # pragma: no cover


class ArtifactsOwned(TrackingRule):
    name = "artifacts-owned"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usernames = set(self._params)

    async def matches(self, message):
        for artifact_type in ArtifactType:
            for artifact in getattr(message, artifact_type.name):
                owners = await self._requester.distgit.get_owners(
                    artifact_type.value, artifact, "user"
                )
                if self.usernames & set(owners):
                    return True
        return False

    async def prime_cache(self, cache):
        for username in self.usernames:
            for artifact_type in ArtifactType:
                owned = await self._requester.distgit.get_owned(
                    artifact_type.value, username, "user"
                )
                getattr(cache, artifact_type.name).update(set(owned))


class ArtifactsGroupOwned(TrackingRule):
    name = "artifacts-group-owned"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.groups = set(self._params)

    async def matches(self, message):
        for artifact_type in ArtifactType:
            for artifact in getattr(message, artifact_type.name):
                owners = await self._requester.distgit.get_owners(
                    artifact_type.value, artifact, "group"
                )
                if self.groups & set(owners):
                    return True
        return False

    async def prime_cache(self, cache):
        for group in self.groups:
            for artifact_type in ArtifactType:
                owned = await self._requester.distgit.get_owned(artifact_type.value, group, "group")
                getattr(cache, artifact_type.name).update(set(owned))


class ArtifactsFollowed(TrackingRule):
    name = "artifacts-followed"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.followed = {
            atype.name: {p["name"] for p in self._params if p["type"] == atype.value}
            for atype in ArtifactType
        }
        # → packages: {"pkg1", "pkg2", "pkg3"}

    async def matches(self, message):
        for msg_attr, followed in self.followed.items():
            if not followed:
                continue
            if set(followed).intersection(set(getattr(message, msg_attr))):
                return True
        return False

    async def prime_cache(self, cache):
        for msg_attr, followed in self.followed.items():
            if not followed:
                continue
            getattr(cache, msg_attr).update(followed)


class RelatedEvents(TrackingRule):
    name = "related-events"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def matches(self, message):
        return self._owner in message.usernames

    async def prime_cache(self, cache):
        cache.usernames.add(self._owner)


class UsersFollowed(TrackingRule):
    name = "users-followed"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.followed = set(self._params)

    async def matches(self, message):
        return message.agent_name in self.followed

    async def prime_cache(self, cache):
        cache.agent_name.update(self.followed)
