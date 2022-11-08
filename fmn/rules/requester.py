import logging
from functools import wraps
from typing import TYPE_CHECKING

import requests

from .services.distgit import DistGitService
from .services.fasjson import FasjsonService

if TYPE_CHECKING:
    from fedora_messaging.message import Message


log = logging.getLogger(__name__)


def handle_http_error(default):
    def exception_handler(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                return f(*args, **kw)
            except requests.HTTPError as e:
                log.warning(f"Request failed: {e}")
                return default

        return wrapper

    return exception_handler


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

    @handle_http_error([])
    def get_owned_by_user(self, artifact_type, username):
        log.debug(f"Getting owned {artifact_type} by {username}")
        return self.distgit_client.get_owned(artifact_type, username, "user")

    @handle_http_error([])
    def get_owned_by_group(self, artifact_type, groupname):
        log.debug(f"Getting owned {artifact_type} by group {groupname}")
        return self.distgit_client.get_owned(artifact_type, groupname, "group")

    @handle_http_error([])
    def get_package_owners(self, name: str):
        log.debug(f"Getting owners of rpms/{name}")
        return self.distgit_client.get_owners("rpms", name, "user")

    @handle_http_error([])
    def get_container_owners(self, name: str):
        log.debug(f"Getting owners of containers/{name}")
        return self.distgit_client.get_owners("containers", name, "user")

    @handle_http_error([])
    def get_module_owners(self, name: str):
        log.debug(f"Getting owners of modules/{name}")
        return self.distgit_client.get_owners("modules", name, "user")

    @handle_http_error([])
    def get_flatpak_owners(self, name: str):
        log.debug(f"Getting owners of flatpaks/{name}")
        return self.distgit_client.get_owners("flatpaks", name, "user")

    @handle_http_error([])
    def get_package_group_owners(self, name: str):
        log.debug(f"Getting group owners of rpms/{name}")
        return self.distgit_client.get_owners("rpms", name, "group")

    @handle_http_error([])
    def get_container_group_owners(self, name: str):
        log.debug(f"Getting group owners of containers/{name}")
        return self.distgit_client.get_owners("containers", name, "group")

    @handle_http_error([])
    def get_module_group_owners(self, name: str):
        log.debug(f"Getting group owners of modules/{name}")
        return self.distgit_client.get_owners("modules", name, "group")

    @handle_http_error([])
    def get_flatpak_group_owners(self, name: str):
        log.debug(f"Getting group owners of flatpaks/{name}")
        return self.distgit_client.get_owners("flatpaks", name, "group")

    @handle_http_error([])
    def get_user_groups(self, name: str):
        log.debug(f"Getting groups of user {name}")
        return self.fasjson_client.get_user_groups(name)

    def invalidate_on_message(self, message: "Message"):
        self.distgit_client.invalidate_on_message(message)
        self.fasjson_client.invalidate_on_message(message)
