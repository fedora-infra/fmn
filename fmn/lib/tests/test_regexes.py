import fmn.lib


class MockContext(object):
    def __init__(self, name):
        self.name = name


email = MockContext('email')
irc = MockContext('irc')


class TestRegexes(fmn.lib.tests.Base):
    def test_valid_emails(self):
        values = [
            'awesome@fedoraproject.org',
            'foo+fedora.org@bar.baz',
        ]

        for value in values:
            # None of these should raise exceptions
            fmn.lib.validate_detail_value(email, value)

    def test_invalid_emails(self):
        values = [
            'wat',
            'not@anemail.org?',
        ]

        for value in values:
            # All of these should raise exceptions
            try:
                fmn.lib.validate_detail_value(email, value)
            except ValueError:
                pass
            else:
                raise ValueError("Invalid email %r did not fail" % value)

    def test_valid_ircnicks(self):
        values = [
            'threebean',
            'awesome|guy',
        ]

        for value in values:
            # None of these should raise exceptions
            fmn.lib.validate_detail_value(irc, value)

    def test_invalid_ircnicks(self):
        values = [
            '?',
        ]

        for value in values:
            # All of these should raise exceptions
            try:
                fmn.lib.validate_detail_value(irc, value)
            except ValueError:
                pass
            else:
                raise ValueError("Invalid ircnick %r did not fail" % value)
