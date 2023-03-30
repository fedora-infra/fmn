# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from unittest.mock import AsyncMock, Mock

import pytest

from fmn.backends import PagureRole
from fmn.cache.tracked import Tracked
from fmn.core.constants import ArtifactType


class MockPagureAsyncProxy:
    async def get_projects(self, *, username):
        return [
            {"namespace": atype.value, "name": f"{atype.value}-{num}"}
            for num in range(1, 3)
            for atype in ArtifactType
        ]

    async def get_user_projects(self, *, username):
        return [
            {"namespace": atype.value, "name": f"{atype.value}-{num}"}
            for num in range(1, 3)
            for atype in ArtifactType
        ]

    async def _get_project_users_groups(self, *, project_path):
        # The mock artifact names are of the form "art-<expected_user_group_name>".
        return [project_path.split("/", 1)[1][4:]]

    get_project_users = get_project_groups = _get_project_users_groups

    async def get_group_projects(self, *, name, acl):
        assert isinstance(name, str)
        assert isinstance(acl, PagureRole)
        return [
            {
                "name": f"{artifact_type.value}-{num}",
                "namespace": artifact_type.value,
                "fullname": f"{artifact_type.value}/{artifact_type.value}-{num}",
                "access_groups": {role.name.lower(): [name] for role in PagureRole.GROUP_ROLES_SET},
            }
            for artifact_type in ArtifactType
            for num in range(1, 3)
        ]


@pytest.fixture
def requester():
    r = Mock(name="requester")
    r.distgit = AsyncMock(name="distgit", wraps=MockPagureAsyncProxy())
    r.fasjson = AsyncMock(name="fasjson")
    r.fasjson.get_user_groups.return_value = ["group1"]
    return r


@pytest.fixture
def cache():
    return Tracked()
