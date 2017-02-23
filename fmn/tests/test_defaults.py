import fmn.lib.models
import fmn.tests


class TestDefaults(fmn.tests.Base):
    def create_data(self):
        fmn.lib.models.Context.create(
            self.sess, name="email", description="the email",
            detail_name="email_address", icon="mail",
        )
        fmn.lib.models.User.get_or_create(
            self.sess,
            openid="ralph.id.fedoraproject.org",
            openid_url="http://ralph.id.fedoraproject.org/",
            create_defaults=True,
            detail_values=dict(email='shmalf@fedoraproject.org'),
        )
        fmn.lib.models.User.get_or_create(
            self.sess,
            openid="toshio.id.fedoraproject.org",
            openid_url="http://toshio.id.fedoraproject.org/",
            create_defaults=True,
        )

    def test_defaults_with_detail_value(self):
        self.create_data()
        preferences = fmn.lib.load_preferences()
        pref = preferences['ralph.id.fedoraproject.org_email']
        self.assertEqual(pref['user']['openid'], 'ralph.id.fedoraproject.org')
        self.assertEqual(pref['detail_values'], ['shmalf@fedoraproject.org'])
        self.assertEqual(pref['enabled'], True)

    def test_defaults_without_detail_value(self):
        self.create_data()
        preferences = fmn.lib.load_preferences()
        pref = preferences['toshio.id.fedoraproject.org_email']
        self.assertEqual(pref['user']['openid'], 'toshio.id.fedoraproject.org')
        self.assertEqual(pref['detail_values'], [])
        self.assertEqual(pref['enabled'], False)
