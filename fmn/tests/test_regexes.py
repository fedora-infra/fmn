import fmn.lib
import fmn.tests
import smtplib


class MockContext(object):
    def __init__(self, name):
        self.name = name


# We rely on a running smtp server somewhere to actually validate our email
# addresses, so we'll mock that out here for our tests.
class MockSMTPServer(object):
    def __init__(self, servername):
        pass

    def verify(self, value):
        if value not in [
            'awesome@fedoraproject.org',
            'foo+fedora.org@bar.baz',
        ]:
            return 500, "failboat"
        else:
            return 250, "all good"


email = MockContext('email')
irc = MockContext('irc')


class TestRegexes(fmn.tests.Base):
    def setUp(self):
        super(TestRegexes, self).setUp()
        self.config = {'fmn.email.mailserver': 'fudgeddaboudit'}
        self.original_smtp = smtplib.SMTP
        smtplib.SMTP = MockSMTPServer

    def tearDown(self):
        super(TestRegexes, self).tearDown()
        smtplib.SMTP = self.original_smtp

    def test_valid_emails(self):
        values = [
            'awesome@fedoraproject.org',
            'foo+fedora.org@bar.baz',
        ]

        for value in values:
            # None of these should raise exceptions
            fmn.lib.validate_detail_value(email, value, self.config)

    def test_invalid_emails(self):
        values = [
            'wat',
            'not@anemail.org?',
        ]

        for value in values:
            # All of these should raise exceptions
            try:
                fmn.lib.validate_detail_value(email, value, self.config)
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
            fmn.lib.validate_detail_value(irc, value, self.config)

    def test_invalid_ircnicks(self):
        values = [
            '?',
        ]

        for value in values:
            # All of these should raise exceptions
            try:
                fmn.lib.validate_detail_value(irc, value, self.config)
            except ValueError:
                pass
            else:
                raise ValueError("Invalid ircnick %r did not fail" % value)
