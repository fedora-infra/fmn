import requests
from fedora_messaging.message import Message

from .services.distgit import DistGitService
from .services.fasjson import FasjsonService


class Requester:
    def __init__(self, config):
        self.req = requests.Session()
        self.urls = {}
        for service, url in config.items():
            if service.endswith("_url"):
                service = service[:-4]
            if not url.endswith("/"):
                url = url + "/"
            self.urls[service] = url
        self.distgit_client = DistGitService(self.urls["distgit"])
        self.fasjson_client = FasjsonService(self.urls["fasjson"])

    def get_owned_by_user(self, artifact_type, username):
        return self.distgit_client.get_owned(artifact_type, username, "user")

    def get_owned_by_group(self, artifact_type, groupname):
        return self.distgit_client.get_owned(artifact_type, groupname, "group")

    def get_package_owners(self, name: str):
        return self.distgit_client.get_owners("rpms", name, "user")

    def get_container_owners(self, name: str):
        return self.distgit_client.get_owners("containers", name, "user")

    def get_module_owners(self, name: str):
        return self.distgit_client.get_owners("modules", name, "user")

    def get_flatpak_owners(self, name: str):
        return self.distgit_client.get_owners("flatpaks", name, "user")

    def get_package_group_owners(self, name: str):
        return self.distgit_client.get_owners("rpms", name, "group")

    def get_container_group_owners(self, name: str):
        return self.distgit_client.get_owners("containers", name, "group")

    def get_module_group_owners(self, name: str):
        return self.distgit_client.get_owners("modules", name, "group")

    def get_flatpak_group_owners(self, name: str):
        return self.distgit_client.get_owners("flatpaks", name, "group")

    def get_user_groups(self, name: str):
        return self.fasjson_client.get_user_groups(name)

    def invalidate_on_message(self, message: Message):
        self.distgit_client.invalidate_on_message(message)
        self.fasjson_client.invalidate_on_message(message)
