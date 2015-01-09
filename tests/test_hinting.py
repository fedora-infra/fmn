import inspect
import unittest

import fmn.rules.bodhi


class TestHinting(unittest.TestCase):
    def test_basic_hinting(self):
        assert fmn.rules.bodhi.bodhi_buildroot_override_tag.hints == {
            'categories': ['bodhi'],
        }
        docs = inspect.getdoc(fmn.rules.bodhi.bodhi_buildroot_override_tag)
        assert 'decorator' not in docs
