from nose.tools import eq_

import fmn.lib.tests


class TestHintDecoration(fmn.lib.tests.Base):
    def test_hint_decoration(self):
        rules = self.valid_paths['fmn.lib.tests.example_rules']
        rule = rules['hint_masked_rule']

        eq_(rule['title'], u'This is a docstring.')

        eq_(len(rule['args']), 3)

        eq_(rule['datanommer-hints'], {'categories': ['whatever']})
