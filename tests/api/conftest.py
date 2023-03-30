# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from unittest import mock

import pytest

import fmn.api.main
from fmn.api.auth import get_identity, get_identity_optional


@pytest.fixture
def api_identity(fasjson_user_data):
    class TestIdentity:
        name = fasjson_user_data["username"]
        admin = False

    def get_test_identity():
        return TestIdentity

    with mock.patch.dict(fmn.api.main.app.dependency_overrides):
        fmn.api.main.app.dependency_overrides[get_identity] = get_test_identity

        yield TestIdentity


@pytest.fixture
def api_identity_optional(fasjson_user_data):
    class TestIdentity:
        name = fasjson_user_data["username"]
        admin = False

    def get_test_identity_optional():
        return TestIdentity

    with mock.patch.dict(fmn.api.main.app.dependency_overrides):
        fmn.api.main.app.dependency_overrides[get_identity_optional] = get_test_identity_optional

        yield TestIdentity
