import pytest


class MockedRequester:
    def _get_owners(self, artifact):
        return [artifact[4:]]

    def _get_group_owner(self, artifact):
        return self._get_owners(artifact)

    def get_user_groups(self, username):
        return ["group1"]

    def get_package_owners(self, artifact):
        return self._get_owners(artifact)

    def get_container_owners(self, artifact):
        return self._get_owners(artifact)

    def get_module_owners(self, artifact):
        return self._get_owners(artifact)

    def get_flatpak_owners(self, artifact):
        return self._get_owners(artifact)

    def get_package_group_owners(self, artifact):
        return self._get_group_owner(artifact)

    def get_container_group_owners(self, artifact):
        return self._get_group_owner(artifact)

    def get_module_group_owners(self, artifact):
        return self._get_group_owner(artifact)

    def get_flatpak_group_owners(self, artifact):
        return self._get_group_owner(artifact)

    def get_owned_by_user(self, artifact_type, username):
        return [f"{artifact_type}-1", f"{artifact_type}-2"]

    def get_owned_by_group(self, artifact_type, group):
        return [f"{artifact_type}-1", f"{artifact_type}-2"]


@pytest.fixture
def requester():
    return MockedRequester()


@pytest.fixture
def cache():
    return {
        "packages": set(),
        "containers": set(),
        "modules": set(),
        "flatpaks": set(),
    }
