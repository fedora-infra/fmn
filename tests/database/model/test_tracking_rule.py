# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from unittest.mock import Mock

import pytest

from fmn.database import model
from fmn.rules.tracking_rules import ArtifactsFollowed


@pytest.fixture
def rule_db():
    return model.Rule(
        name="testrule",
        user=model.User(name="testuser"),
        generation_rules=[],
    )


def test_get_implementation(rule_db):
    requester = Mock()
    tr = model.TrackingRule(name="artifacts-followed", params={}, rule=rule_db)
    impl = tr.get_implementation(requester)
    assert isinstance(impl, ArtifactsFollowed)


def test_get_implementation_ep_not_found(mocker, rule_db):
    mocker.patch("fmn.database.model.tracking_rule.entry_points", return_value=[])
    requester = Mock()
    tr = model.TrackingRule(name="artifacts-followed", params={}, rule=rule_db)
    with pytest.raises(ValueError):
        tr.get_implementation(requester)


def test_get_implementation_conflicting_eps(mocker, rule_db):
    mocker.patch("fmn.database.model.tracking_rule.entry_points", return_value=["ep1", "ep2"])
    requester = Mock()
    tr = model.TrackingRule(name="artifacts-followed", params={}, rule=rule_db)
    with pytest.raises(ValueError):
        tr.get_implementation(requester)


async def test_prime_cache(mocker, rule_db):
    cache = Mock(name="cache")
    requester = Mock(name="requester")
    tr = model.TrackingRule(name="artifacts-followed", params={}, rule=rule_db)
    impl_prime_cache = mocker.patch.object(ArtifactsFollowed, "prime_cache")
    await tr.prime_cache(cache, requester)
    impl_prime_cache.assert_called_once_with(cache)
