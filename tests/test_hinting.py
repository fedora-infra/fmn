import inspect
import unittest

import fmn.rules.bodhi


class TestHinting(unittest.TestCase):
    def test_basic_hinting(self):
        hints = fmn.rules.bodhi.bodhi_buildroot_override_tag.hints
        assert hints.keys() == ['topics']
        assert hints['topics']  # Make sure it has something in there

        docs = inspect.getdoc(fmn.rules.bodhi.bodhi_buildroot_override_tag)
        assert 'decorator' not in docs
