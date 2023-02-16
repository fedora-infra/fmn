import pytest


@pytest.mark.usefixtures("mocked_fasjson", "mocked_fasjson_proxy")
class BaseTestHandler:
    api_prefix = None
    handler_prefix = None

    @property
    def path(self):
        return (self.api_prefix or "") + (self.handler_prefix or "")


class BaseTestAPIV1Handler(BaseTestHandler):
    api_prefix = "/api/v1"
