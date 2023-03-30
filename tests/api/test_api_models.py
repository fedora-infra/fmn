# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from unittest import mock

from fmn.api.api_models import GRGetterDict


class TestGRGetterDict:
    def test_get(self):
        filter_obj = mock.Mock()
        filter_obj.name = "filter"
        filter_obj.params = {"this is": "params"}

        processed_obj = mock.Mock(foo="bar", filters=[filter_obj])
        del processed_obj.boop

        getter_dict = GRGetterDict(processed_obj)

        default_sentinel = object()

        assert getter_dict.get("boop", default_sentinel) is default_sentinel
        assert getter_dict.get("foo", default_sentinel) == "bar"
        assert getter_dict.get("filters", default_sentinel) == {"filter": {"this is": "params"}}
