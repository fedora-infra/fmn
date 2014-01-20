from nose.tools import eq_, assert_not_equals

import os
import fmn.lib.models
import fmn.lib.tests


class TestConfirmations(fmn.lib.tests.Base):
    def create_user_and_context_data(self):
        user1 = fmn.lib.models.User.get_or_create(
            self.sess, openid="ralph.id.fedoraproject.org",
            openid_url="http://ralph.id.fedoraproject.org/",
        )
        context1 = fmn.lib.models.Context.create(
            self.sess, name="irc", description="Internet Relay Chat",
            detail_name="irc nick", icon="user",
        )

    def create_preference_data_empty(self):
        user = fmn.lib.models.User.get(
            self.sess, openid="ralph.id.fedoraproject.org")
        context = fmn.lib.models.Context.get(self.sess, name="irc")
        preference = fmn.lib.models.Preference.create(
            self.sess,
            user=user,
            context=context,
            detail_value=None,
        )

    def test_updating_details(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()
        user = fmn.lib.models.User.get(
            self.sess, openid="ralph.id.fedoraproject.org")
        context = fmn.lib.models.Context.get(self.sess, name="irc")
        preference = fmn.lib.models.Preference.load(self.sess, user, context)
        preference.update_details(self.sess, 'wat')
        eq_(preference.detail_values[0].value, 'wat')
        preference.update_details(self.sess, 'wat2')
        eq_(preference.detail_values[0].value, 'wat')
        eq_(preference.detail_values[1].value, 'wat2')

        try:
            preference.update_details(self.sess, 'wat')
            assert(False)
        except Exception:
            self.sess.rollback()

        eq_(len(preference.detail_values), 2)
        eq_(preference.detail_values[0].value, 'wat')
        eq_(preference.detail_values[1].value, 'wat2')

    def test_confirmation(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()
        user = fmn.lib.models.User.get(
            self.sess, openid="ralph.id.fedoraproject.org")
        context = fmn.lib.models.Context.get(self.sess, name="irc")
        preference = fmn.lib.models.Preference.load(self.sess, user, context)
        confirmation = fmn.lib.models.Confirmation.create(
            self.sess,
            user,
            context,
            detail_value='awesome',
        )
        eq_(preference.detail_values, [])
        confirmation.set_status(self.sess, 'accepted')
        eq_(preference.detail_values[0].value, 'awesome')
