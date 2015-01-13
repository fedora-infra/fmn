from nose.tools import eq_, assert_not_equals

import fmn.lib.tests


class TestDefaults(fmn.lib.tests.Base):
    def test_hint_decoration(self):
        rules = self.valid_paths['fmn.lib.tests.example_rules']
        rule = rules['hint_masked_rule']
        import pprint;
        pprint.pprint(rule)
        eq_(rule['title'], u'This is a docstring.')
        eq_(len(rule['args']), 1)
