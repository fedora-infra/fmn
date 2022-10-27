from unittest.mock import Mock

import pytest

from fmn.database import model
from fmn.rules.tracking_rules import ArtifactsFollowed


def test_get_implementation():
    requester = Mock()
    tr = model.TrackingRule(name="artifacts-followed", params={})
    impl = tr.get_implementation(requester)
    assert isinstance(impl, ArtifactsFollowed)


def test_get_implementation_ep_not_found(mocker):
    mocker.patch("fmn.database.model.tracking_rule.entry_points", return_value=[])
    requester = Mock()
    tr = model.TrackingRule(name="artifacts-followed", params={})
    with pytest.raises(ValueError):
        tr.get_implementation(requester)


def test_get_implementation_conflicting_eps(mocker):
    mocker.patch("fmn.database.model.tracking_rule.entry_points", return_value=["ep1", "ep2"])
    requester = Mock()
    tr = model.Filter(name="artifacts-followed", params={})
    with pytest.raises(ValueError):
        tr.get_implementation(requester)


def test_prime_cache(mocker):
    cache = Mock(name="cache")
    requester = Mock(name="requester")
    tr = model.TrackingRule(name="artifacts-followed", params={})
    impl_prime_cache = mocker.patch.object(ArtifactsFollowed, "prime_cache")
    tr.prime_cache(cache, requester)
    impl_prime_cache.assert_called_once_with(cache)
