from nose.tools import eq_, assert_not_equals

import os
import fmn.lib.models
import fmn.lib.tests


class TestRecipients(fmn.lib.tests.Base):
    def create_user_and_context_data(self):
        user1 = fmn.lib.models.User.get_or_create(
            self.sess, openid="ralph.id.fedoraproject.org")
        user2 = fmn.lib.models.User.get_or_create(
            self.sess, openid="toshio.id.fedoraproject.org")
        context1 = fmn.lib.models.Context.create(
            self.sess, name="irc", description="Internet Relay Chat",
            detail_name="irc nick", icon="user",
        )
        context2 = fmn.lib.models.Context.create(
            self.sess, name="android", description="Google Cloud Messaging",
            detail_name="registration id", icon="phone",
        )

    def create_preference_data_empty(self):
        user = fmn.lib.models.User.get(
            self.sess, openid="ralph.id.fedoraproject.org")
        context = fmn.lib.models.Context.get(self.sess, name="irc")
        preference = fmn.lib.models.Preference.create(
            self.sess,
            user=user,
            context=context,
            detail_value="threebean",
        )

    def create_preference_data_basic(self, code_path):
        user = fmn.lib.models.User.get(
            self.sess, openid="ralph.id.fedoraproject.org")
        context = fmn.lib.models.Context.get(self.sess, name="irc")
        preference = fmn.lib.models.Preference.load(self.sess, user, context)
        chain = fmn.lib.models.Chain.create(self.sess, name="test chain")
        chain.add_filter(self.sess, self.valid_paths, code_path)
        preference.add_chain(self.sess, chain)

    def test_empty_recipients_list(self):
        self.create_user_and_context_data()
        incoming_message = {
            "wat": "blah",
        }
        recipients = fmn.lib.recipients(
            self.sess, self.config, incoming_message)
        expected_keys = set(['irc', 'android'])
        eq_(set(recipients.keys()), expected_keys)
        eq_(list(recipients['irc']), [])
        eq_(list(recipients['android']), [])

    def test_empty_recipients_list(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()
        msg = {
            "wat": "blah",
        }
        recipients = fmn.lib.recipients_for_context(
            self.sess, self.config, self.valid_paths, 'android', msg)
        eq_(list(recipients), [])

    def test_basic_recipients_list(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()

        code_path = "fmn.lib.tests.example_filters:wat_filter"
        self.create_preference_data_basic(code_path)

        msg = {
            "wat": "blah",
        }
        recipients = fmn.lib.recipients_for_context(
            self.sess, self.config, self.valid_paths, 'irc', msg)
        eq_(list(recipients), [{
            'irc nick': 'threebean',
            'user': 'ralph.id.fedoraproject.org',
            'chain': 'test chain',
            }])

    def test_miss_recipients_list(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()

        code_path = "fmn.lib.tests.example_filters:not_wat_filter"
        self.create_preference_data_basic(code_path)

        msg = {
            "wat": "blah",
        }
        recipients = fmn.lib.recipients_for_context(
            self.sess, self.config, self.valid_paths, 'irc', msg)
        eq_(list(recipients), [])

    def test_multiple_identical_chains_miss(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()

        # Tack two identical chains onto the preferenced
        code_path = "fmn.lib.tests.example_filters:not_wat_filter"
        self.create_preference_data_basic(code_path)
        code_path = "fmn.lib.tests.example_filters:not_wat_filter"
        self.create_preference_data_basic(code_path)

        preference = fmn.lib.models.Preference.load(
            self.sess, "ralph.id.fedoraproject.org", "irc")
        eq_(len(preference.chains), 2)

        msg = {
            "wat": "blah",
        }
        recipients = fmn.lib.recipients_for_context(
            self.sess, self.config, self.valid_paths, 'irc', msg)
        eq_(list(recipients), [])

    def test_multiple_identical_chains_hit(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()

        # Tack two identical chains onto the preferenced
        code_path = "fmn.lib.tests.example_filters:wat_filter"
        self.create_preference_data_basic(code_path)
        code_path = "fmn.lib.tests.example_filters:wat_filter"
        self.create_preference_data_basic(code_path)

        preference = fmn.lib.models.Preference.load(
            self.sess, "ralph.id.fedoraproject.org", "irc")
        eq_(len(preference.chains), 2)

        msg = {
            "wat": "blah",
        }
        recipients = fmn.lib.recipients_for_context(
            self.sess, self.config, self.valid_paths, 'irc', msg)
        eq_(list(recipients), [{
            'irc nick': 'threebean',
            'user': 'ralph.id.fedoraproject.org',
            'chain': 'test chain',
            }])

    def test_multiple_different_chains_hit(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()

        # Tack two identical chains onto the preferenced
        code_path = "fmn.lib.tests.example_filters:wat_filter"
        self.create_preference_data_basic(code_path)
        code_path = "fmn.lib.tests.example_filters:not_wat_filter"
        self.create_preference_data_basic(code_path)

        preference = fmn.lib.models.Preference.load(
            self.sess, "ralph.id.fedoraproject.org", "irc")
        eq_(len(preference.chains), 2)

        msg = {
            "wat": "blah",
        }
        recipients = fmn.lib.recipients_for_context(
            self.sess, self.config, self.valid_paths, 'irc', msg)
        eq_(list(recipients), [{
            'irc nick': 'threebean',
            'user': 'ralph.id.fedoraproject.org',
            'chain': 'test chain',
            }])
