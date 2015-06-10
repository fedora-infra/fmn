from nose.tools import eq_

import fmn.lib
import fmn.lib.hinting
import fmn.lib.tests


class TestHintDecoration(fmn.lib.tests.Base):
    def test_hint_decoration(self):
        rules = self.valid_paths['fmn.lib.tests.example_rules']
        rule = rules['hint_masked_rule']

        eq_(rule['title'], u'This is a docstring.')

        eq_(len(rule['args']), 3)

        eq_(rule['datanommer-hints'], {'categories': ['whatever']})

    def test_hint_callable(self):
        rules = self.valid_paths['fmn.lib.tests.example_rules']
        rule = rules['callable_hint_masked_rule']
        eq_(len(rule['args']), 3)
        eq_(rule['datanommer-hints'], {})

        class MockRule(object):
            code_path = 'fmn.lib.tests.example_rules:callable_hint_masked_rule'
            arguments = {
                'argument1': 'cowabunga',
            }
            negated = False

        rules = [MockRule()]

        hints = fmn.lib.hinting.gather_hinting(
            self.config, rules, self.valid_paths)
        eq_(hints, {'the-hint-is': ['cowabunga']})

    def test_inverted_hint_callable(self):
        rules = self.valid_paths['fmn.lib.tests.example_rules']
        rule = rules['callable_hint_masked_rule']
        eq_(len(rule['args']), 3)
        eq_(rule['datanommer-hints'], {})

        class MockRule(object):
            code_path = 'fmn.lib.tests.example_rules:callable_hint_masked_rule'
            arguments = {
                'argument1': 'cowabunga',
            }
            negated = True

        rules = [MockRule()]

        hints = fmn.lib.hinting.gather_hinting(
            self.config, rules, self.valid_paths)
        eq_(hints, {'not_the-hint-is': ['cowabunga']})
