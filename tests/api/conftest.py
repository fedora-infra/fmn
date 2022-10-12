from unittest import mock

import pytest

import fmn.api.main
from fmn.api.auth import get_identity


@pytest.fixture
def api_identity(fasjson_user_data):
    class TestIdentity:
        name = fasjson_user_data["username"]

    def get_test_identity():
        return TestIdentity

    with mock.patch.dict(fmn.api.main.app.dependency_overrides):
        fmn.api.main.app.dependency_overrides[get_identity] = get_test_identity

        yield TestIdentity
