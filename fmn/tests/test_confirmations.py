import fmn.lib.models
import fmn.tests


class TestConfirmations(fmn.tests.Base):
    def create_user_and_context_data(self):
        fmn.lib.models.User.get_or_create(
            self.sess, openid="ralph.id.fedoraproject.org",
            openid_url="http://ralph.id.fedoraproject.org/",
        )
        fmn.lib.models.Context.create(
            self.sess, name="irc", description="Internet Relay Chat",
            detail_name="irc nick", icon="user",
        )

    def create_preference_data_empty(self):
        user = fmn.lib.models.User.get(
            self.sess, openid="ralph.id.fedoraproject.org")
        context = fmn.lib.models.Context.get(self.sess, name="irc")
        fmn.lib.models.Preference.create(
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
        self.assertEqual(preference.detail_values[0].value, 'wat')
        preference.update_details(self.sess, 'wat2')
        self.assertEqual(preference.detail_values[0].value, 'wat')
        self.assertEqual(preference.detail_values[1].value, 'wat2')

        try:
            preference.update_details(self.sess, 'wat')
            assert(False)
        except Exception:
            self.sess.rollback()

        self.assertEqual(len(preference.detail_values), 2)
        self.assertEqual(preference.detail_values[0].value, 'wat')
        self.assertEqual(preference.detail_values[1].value, 'wat2')

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
        self.assertEqual(preference.detail_values, [])
        confirmation.set_status(self.sess, 'accepted')
        self.assertEqual(preference.detail_values[0].value, 'awesome')
