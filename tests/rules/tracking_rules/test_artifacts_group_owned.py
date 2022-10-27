import pytest

from fmn.rules.tracking_rules import ArtifactsGroupOwned


@pytest.mark.parametrize(
    "artifact_type",
    [
        "packages",
        "containers",
        "modules",
        "flatpaks",
    ],
)
def test_artifacts_group_owned(requester, make_mocked_message, artifact_type):
    tr = ArtifactsGroupOwned(requester, {"username": "dummy", "groups": None})
    message = make_mocked_message(topic="dummy", body={artifact_type: ["art-group1", "art-group2"]})
    assert tr.matches(message) is True
    message = make_mocked_message(topic="dummy", body={artifact_type: ["art-group2"]})
    assert tr.matches(message) is False


def test_artifacts_group_owned_cache(requester, cache):
    tr = ArtifactsGroupOwned(requester, {"username": "dummy", "groups": None})
    tr.prime_cache(cache)
    assert cache == {
        "packages": set(["package-1", "package-2"]),
        "containers": set(["container-1", "container-2"]),
        "modules": set(["module-1", "module-2"]),
        "flatpaks": set(["flatpak-1", "flatpak-2"]),
    }
