from nose.tools import eq_, assert_not_equals

import os
import fmn.lib.models
import fmn.lib.tests


class TestDefaults(fmn.lib.tests.Base):
    def create_data(self):
        context = fmn.lib.models.Context.create(
            self.sess, name="email", description="the email",
            detail_name="email_address", icon="mail",
        )
        user1 = fmn.lib.models.User.get_or_create(
            self.sess,
            openid="ralph.id.fedoraproject.org",
            openid_url="http://ralph.id.fedoraproject.org/",
            create_defaults=True,
            detail_values=dict(email='shmalf@fedoraproject.org'),
        )
        user2 = fmn.lib.models.User.get_or_create(
            self.sess,
            openid="toshio.id.fedoraproject.org",
            openid_url="http://toshio.id.fedoraproject.org/",
            create_defaults=True,
        )

    def test_defaults_with_detail_value(self):
        self.create_data()
        preferences = fmn.lib.load_preferences(
            self.sess, self.config, self.valid_paths)
        pref = preferences[0]
        eq_(pref['user']['openid'], 'ralph.id.fedoraproject.org')
        eq_(pref['detail_values'], ['shmalf@fedoraproject.org'])
        eq_(pref['enabled'], True)

    def test_defaults_without_detail_value(self):
        self.create_data()
        preferences = fmn.lib.load_preferences(
            self.sess, self.config, self.valid_paths)
        pref = preferences[1]
        eq_(pref['user']['openid'], 'toshio.id.fedoraproject.org')
        eq_(pref['detail_values'], [])
        eq_(pref['enabled'], False)
