from nose.tools import eq_, assert_not_equals

import os
import fmn.lib.models
import fmn.lib.tests


class TestRecipients(fmn.lib.tests.Base):
    def setUp(self):
        super(TestRecipients, self).setUp()

    def create_user_and_context_data(self):
        user1 = fmn.lib.models.User.get_or_create(
            self.sess, openid="ralph.id.fedoraproject.org",
            openid_url="http://ralph.id.fedoraproject.org/",
        )
        user2 = fmn.lib.models.User.get_or_create(
            self.sess, openid="toshio.id.fedoraproject.org",
            openid_url="http://toshio.id.fedoraproject.org/",
        )
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
        preference.enabled = False

        user = fmn.lib.models.User.get(
            self.sess, openid="toshio.id.fedoraproject.org")
        context = fmn.lib.models.Context.get(self.sess, name="irc")
        preference = fmn.lib.models.Preference.create(
            self.sess,
            user=user,
            context=context,
            detail_value="abadger1999",
        )

    def create_preference_data_basic(self, code_path):
        user = fmn.lib.models.User.get(
            self.sess, openid="ralph.id.fedoraproject.org")
        context = fmn.lib.models.Context.get(self.sess, name="irc")
        preference = fmn.lib.models.Preference.load(self.sess, user, context)
        filter = fmn.lib.models.Filter.create(self.sess, name="test filter")
        filter.add_rule(self.sess, self.valid_paths, code_path)
        preference.add_filter(self.sess, filter)

        user = fmn.lib.models.User.get(
            self.sess, openid="toshio.id.fedoraproject.org")
        context = fmn.lib.models.Context.get(self.sess, name="irc")
        preference = fmn.lib.models.Preference.load(self.sess, user, context)
        filter = fmn.lib.models.Filter.create(self.sess, name="test filter 2")
        filter.add_rule(self.sess, self.valid_paths, code_path)
        preference.add_filter(self.sess, filter)

    def test_empty_recipients_list(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()

        msg = {
            "wat": "blah",
        }
        preferences = fmn.lib.load_preferences(
            self.sess, self.config, self.valid_paths)
        recipients = fmn.lib.recipients(
            preferences, msg, self.valid_paths, self.config)
        eq_(recipients, {})

    def test_basic_recipients_list(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()

        code_path = "fmn.lib.tests.example_rules:wat_rule"
        self.create_preference_data_basic(code_path)

        msg = {
            "wat": "blah",
        }
        preferences = fmn.lib.load_preferences(
            self.sess, self.config, self.valid_paths)
        recipients = fmn.lib.recipients(
            preferences, msg, self.valid_paths, self.config)
        self.assertDictEqual(recipients['irc'][0], {
            'triggered_by_links': True,
            'markup_messages': False,
            'shorten_links': False,
            'irc nick': 'threebean',
            'user': 'ralph.id.fedoraproject.org',
            'filter_name': 'test filter',
            'filter_id': 1,
            'filter_oneshot': False,
            'verbose': True,
        })

    def test_miss_recipients_list(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()

        code_path = "fmn.lib.tests.example_rules:not_wat_rule"
        self.create_preference_data_basic(code_path)

        msg = {
            "wat": "blah",
        }
        preferences = fmn.lib.load_preferences(
            self.sess, self.config, self.valid_paths)
        recipients = fmn.lib.recipients(
            preferences, msg, self.valid_paths, self.config)
        eq_(recipients, {})

    def test_multiple_identical_filters_miss(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()

        # Tack two identical filters onto the preferenced
        code_path = "fmn.lib.tests.example_rules:not_wat_rule"
        self.create_preference_data_basic(code_path)
        code_path = "fmn.lib.tests.example_rules:not_wat_rule"
        self.create_preference_data_basic(code_path)

        preference = fmn.lib.models.Preference.load(
            self.sess, "ralph.id.fedoraproject.org", "irc")
        eq_(len(preference.filters), 2)

        msg = {
            "wat": "blah",
        }
        preferences = fmn.lib.load_preferences(
            self.sess, self.config, self.valid_paths)
        recipients = fmn.lib.recipients(
            preferences, msg, self.valid_paths, self.config)
        eq_(recipients, {})

    def test_multiple_identical_filters_hit(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()

        # Tack two identical filters onto the preferenced
        code_path = "fmn.lib.tests.example_rules:wat_rule"
        self.create_preference_data_basic(code_path)
        code_path = "fmn.lib.tests.example_rules:wat_rule"
        self.create_preference_data_basic(code_path)

        preference = fmn.lib.models.Preference.load(
            self.sess, "ralph.id.fedoraproject.org", "irc")
        eq_(len(preference.filters), 2)

        msg = {
            "wat": "blah",
        }
        preferences = fmn.lib.load_preferences(
            self.sess, self.config, self.valid_paths)
        recipients = fmn.lib.recipients(
            preferences, msg, self.valid_paths, self.config)
        expected = {
            'triggered_by_links': True,
            'markup_messages': False,
            'shorten_links': False,
            'irc nick': 'threebean',
            'user': 'ralph.id.fedoraproject.org',
            'filter_name': 'test filter',
            'filter_id': 1,
            'filter_oneshot': False,
            'verbose': True,
        }
        self.assertDictEqual(recipients['irc'][0], expected)

    def test_multiple_different_filters_hit(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()

        # Tack two identical filters onto the preferenced
        code_path = "fmn.lib.tests.example_rules:wat_rule"
        self.create_preference_data_basic(code_path)
        code_path = "fmn.lib.tests.example_rules:not_wat_rule"
        self.create_preference_data_basic(code_path)

        preference = fmn.lib.models.Preference.load(
            self.sess, "ralph.id.fedoraproject.org", "irc")
        eq_(len(preference.filters), 2)

        msg = {
            "wat": "blah",
        }
        preferences = fmn.lib.load_preferences(
            self.sess, self.config, self.valid_paths)
        recipients = fmn.lib.recipients(
            preferences, msg, self.valid_paths, self.config)
        self.assertDictEqual(recipients['irc'][0], {
            'triggered_by_links': True,
            'markup_messages': False,
            'shorten_links': False,
            'irc nick': 'threebean',
            'user': 'ralph.id.fedoraproject.org',
            'filter_name': 'test filter',
            'filter_id': 1,
            'filter_oneshot': False,
            'verbose': True,
        })

    def test_load_preferences(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()
        code_path = "fmn.lib.tests.example_rules:wat_rule"
        self.create_preference_data_basic(code_path)

        preferences = fmn.lib.load_preferences(
            self.sess, self.config, self.valid_paths)

        eq_(len(preferences), 2)
        pref = preferences[0]
        eq_(pref['enabled'], False)
        eq_(pref['user']['openid'], u'ralph.id.fedoraproject.org')
        eq_(pref['context']['name'], u'irc')
        eq_(len(pref['filters']), 1)

    def test_load_preferences_sans_disabled(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()
        code_path = "fmn.lib.tests.example_rules:wat_rule"
        self.create_preference_data_basic(code_path)

        preferences = fmn.lib.load_preferences(
            self.sess, self.config, self.valid_paths, cull_disabled=True)

        eq_(len(preferences), 1)
        pref = preferences[0]
        eq_(pref['enabled'], True)
        eq_(pref['user']['openid'], u'toshio.id.fedoraproject.org')
        eq_(pref['context']['name'], u'irc')
        eq_(len(pref['filters']), 1)
