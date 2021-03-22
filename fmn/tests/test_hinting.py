import inspect
import unittest

import fmn.lib
import fmn.lib.hinting
import fmn.tests
import fmn.rules
import fmn.rules.bodhi


class TestHinting(unittest.TestCase):
    def test_basic_hinting(self):
        hints = fmn.rules.bodhi.bodhi_buildroot_override_tag.hints
        assert list(hints.keys()) == ['topics']
        assert hints['topics']  # Make sure it has something in there

        docs = inspect.getdoc(fmn.rules.bodhi.bodhi_buildroot_override_tag)
        assert 'decorator' not in docs

    def test_all_invertible_topics(self):
        empty_config = {}
        rules = fmn.lib.load_rules('fmn.rules')['fmn.rules']
        for name, rule in rules.items():
            if not rule['datanommer-hints']:
                continue
            if not rule['hints-invertible']:
                continue
            if 'topics' not in rule['datanommer-hints']:
                continue
            topics = rule['datanommer-hints']['topics']
            for topic in topics:
                fake_msg = dict(topic=topic)
                if not rule['func'](empty_config, fake_msg):
                    raise ValueError('%r failed %r' % (topic, rule['title']))


class TestHintDecoration(fmn.tests.Base):
    def test_hint_decoration(self):
        rules = self.valid_paths['fmn.tests.example_rules']
        rule = rules['hint_masked_rule']

        self.assertEqual(rule['title'], u'This is a docstring.')

        self.assertEqual(len(rule['args']), 3)

        self.assertEqual(rule['datanommer-hints'], {'categories': ['whatever']})

    def test_hint_callable(self):
        rules = self.valid_paths['fmn.tests.example_rules']
        rule = rules['callable_hint_masked_rule']
        self.assertEqual(len(rule['args']), 3)
        self.assertEqual(rule['datanommer-hints'], {})

        class MockRule(object):
            code_path = 'fmn.tests.example_rules:callable_hint_masked_rule'
            arguments = {
                'argument1': 'cowabunga',
            }
            negated = False

        rules = [MockRule()]

        hints = fmn.lib.hinting.gather_hinting(
            self.config, rules, self.valid_paths)
        self.assertEqual(hints, {'the-hint-is': ['cowabunga']})

    def test_inverted_hint_callable(self):
        rules = self.valid_paths['fmn.tests.example_rules']
        rule = rules['callable_hint_masked_rule']
        self.assertEqual(len(rule['args']), 3)
        self.assertEqual(rule['datanommer-hints'], {})

        class MockRule(object):
            code_path = 'fmn.tests.example_rules:callable_hint_masked_rule'
            arguments = {
                'argument1': 'cowabunga',
            }
            negated = True

        rules = [MockRule()]

        hints = fmn.lib.hinting.gather_hinting(
            self.config, rules, self.valid_paths)
        self.assertEqual(hints, {'not_the-hint-is': ['cowabunga']})
