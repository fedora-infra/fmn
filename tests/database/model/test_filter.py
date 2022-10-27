from unittest.mock import Mock

import pytest

from fmn.database import model
from fmn.rules.filter import NotMyActions


def test_get_implementation():
    requester = Mock()
    f = model.Filter(name="not_my_actions")
    impl = f.get_implementation(requester)
    assert isinstance(impl, NotMyActions)


def test_get_implementation_ep_not_found(mocker):
    mocker.patch("fmn.database.model.filter.entry_points", return_value=[])
    requester = Mock()
    f = model.Filter(name="not_my_actions")
    with pytest.raises(ValueError):
        f.get_implementation(requester)


def test_get_implementation_conflicting_eps(mocker):
    mocker.patch("fmn.database.model.filter.entry_points", return_value=["ep1", "ep2"])
    requester = Mock()
    f = model.Filter(name="not_my_actions")
    with pytest.raises(ValueError):
        f.get_implementation(requester)
