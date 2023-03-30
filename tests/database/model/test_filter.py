# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from unittest.mock import Mock

import pytest

from fmn.database import model
from fmn.rules.filter import Applications


def test_get_implementation(db_rule):
    requester = Mock()
    f = db_rule.generation_rules[0].filters[0]
    impl = f.get_implementation(requester)
    assert isinstance(impl, Applications)
    assert f.params == ["koji", "bodhi"]


def test_get_implementation_ep_not_found(mocker):
    mocker.patch("fmn.database.model.filter.entry_points", return_value=[])
    requester = Mock()
    f = model.Filter(name="my_actions")
    with pytest.raises(ValueError):
        f.get_implementation(requester)


def test_get_implementation_conflicting_eps(mocker):
    mocker.patch("fmn.database.model.filter.entry_points", return_value=["ep1", "ep2"])
    requester = Mock()
    f = model.Filter(name="my_actions")
    with pytest.raises(ValueError):
        f.get_implementation(requester)
