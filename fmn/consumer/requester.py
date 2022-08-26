import requests
from fasjson_client import Client as FasjsonClient

from .cache import cache


class Requester:
    def __init__(self, config):
        self.req = requests.Session()
        self.urls = {}
        for service, url in config.items():
            if not url.endswith("/"):
                url = url + "/"
            self.urls[service] = url
        self.fasjson_client = FasjsonClient(self.urls["fasjson"])

    @cache.cache_on_arguments(namespace="urlget")
    def _get(self, url, params=None):
        result = self.req.get(url=url, params=params)
        result.raise_for_status()
        return result.json()

    def _owners_from_distgit(self, namespace, artifact_name, user_or_group):
        # cache this for a reasonable time
        url = f"{self.url['distgit']}api/0/{namespace}/{artifact_name}"
        response = self._get(url)
        if user_or_group == "user":
            return response["access_users"]["owner"]
        elif user_or_group == "group":
            return response["access_groups"]["commit"]
        else:
            raise ValueError("Argument user_or_group must be either user or group, duh.")

    def get_package_owners(self, name: str):
        return self._owners_from_distgit("rpms", name, "user")

    def get_container_owners(self, name: str):
        return self._owners_from_distgit("containers", name, "user")

    def get_module_owners(self, name: str):
        return self._owners_from_distgit("modules", name, "user")

    def get_flatpak_owners(self, name: str):
        return self._owners_from_distgit("flatpaks", name, "user")

    def get_package_group_owners(self, name: str):
        return self._owners_from_distgit("rpms", name, "group")

    def get_container_group_owners(self, name: str):
        return self._owners_from_distgit("containers", name, "group")

    def get_module_group_owners(self, name: str):
        return self._owners_from_distgit("modules", name, "group")

    def get_flatpak_group_owners(self, name: str):
        return self._owners_from_distgit("flatpaks", name, "group")

    @cache.cache_on_arguments(namespace="user_groups")
    def get_user_groups(self, name: str):
        return [g["groupname"] for g in self.fasjson_client.list_user_groups(username=name).result]
