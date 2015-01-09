import inspect
import unittest

import fmn.rules
import fmn.rules.bodhi


class TestHinting(unittest.TestCase):
    def test_basic_hinting(self):
        hints = fmn.rules.bodhi.bodhi_buildroot_override_tag.hints
        assert hints.keys() == ['topics']
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
            if not 'topics' in rule['datanommer-hints']:
                continue
            topics = rule['datanommer-hints']['topics']
            for topic in topics:
                fake_msg = dict(topic=topic)
                if not rule['func'](empty_config, fake_msg):
                    raise ValueError('%r failed %r' % (topic, rule['title']))
