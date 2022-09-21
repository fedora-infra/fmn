import pytest
from fedora_messaging import message

from fmn.consumer.cache import cache
from fmn.core.config import get_settings


class Message(message.Message):
    @property
    def summary(self):
        return self.body.get("summary", f"Message on {self.topic}")

    def __str__(self):
        return self.body.get("content", f"Body of message on {self.topic}")

    @property
    def app_name(self):
        return self.body["app"]

    @property
    def author(self):
        return self.body["author"]

    @property
    def usernames(self):
        return self.body.get("usernames", [])

    @property
    def agent_name(self):
        return self.body.get("agent_name")

    @property
    def packages(self):
        return self.body.get("packages", [])

    @property
    def containers(self):
        return self.body.get("containers", [])

    @property
    def modules(self):
        return self.body.get("modules", [])

    @property
    def flatpaks(self):
        return self.body.get("flatpaks", [])


@pytest.fixture(autouse=True)
def register_message_class():
    message._schema_name_to_class["testmessage"] = Message
    message._class_to_schema_name[Message] = "testmessage"
    yield
    del message._schema_name_to_class["testmessage"]
    del message._class_to_schema_name[Message]


@pytest.fixture(autouse=True, scope="session")
def configured_cache():
    cache.configure(**get_settings().dict()["cache"])
