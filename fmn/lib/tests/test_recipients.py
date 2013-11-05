from nose.tools import eq_, assert_not_equals

import os
import fmn.lib.models
import fmn.lib.tests


class TestRecipients(fmn.lib.tests.Base):
    def create_user_and_context_data(self):
        user1 = fmn.lib.models.User.get_or_create(self.sess, username="ralph")
        user2 = fmn.lib.models.User.get_or_create(self.sess, username="toshio")
        context1 = fmn.lib.models.Context.create(
            self.sess, name="irc", description="Internet Relay Chat")
        context2 = fmn.lib.models.Context.create(
            self.sess, name="gcm", description="Google Cloud Messaging")

    def create_preference_data_basic(self):
        user = fmn.lib.models.User.get(self.sess, username="ralph")
        context = fmn.lib.models.Context.get(self.sess, name="irc")
        preference = fmn.lib.models.Preference.create(
            self.sess,
            user=user,
            context=context,
            delivery_detail=dict(
                ircnick="threebean",
            )
        )

    def test_empty_recipients_list(self):
        self.create_user_and_context_data()
        incoming_message = {
            "wat": "blah",
        }
        recipients = fmn.lib.recipients(
            self.sess, self.config, incoming_message)
        expected_keys = set(['irc', 'gcm'])
        eq_(set(recipients.keys()), expected_keys)
        eq_(list(recipients['irc']), [])
        eq_(list(recipients['gcm']), [])

    def test_basic_recipients_list(self):
        self.create_user_and_context_data()
        self.create_preference_data_basic()
        msg = {
            "wat": "blah",
        }
        recipients = fmn.lib.recipients_for_context(
            self.sess, self.config, 'irc', msg)
        eq_(list(recipients), [dict(ircnick="threebean", user="ralph")])

    def test_miss_recipients_list(self):
        self.create_user_and_context_data()
        self.create_preference_data_basic()
        msg = {
            "wat": "blah",
        }
        recipients = fmn.lib.recipients_for_context(
            self.sess, self.config, 'gcm', msg)
        eq_(list(recipients), [])
