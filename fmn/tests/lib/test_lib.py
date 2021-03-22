# -*- coding: utf-8 -*-
#
# This file is part of the FMN project.
# Copyright (C) 2017 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""
Unit tests for the :mod:`fmn.lib` module
"""

import unittest

import mock

from fmn.lib import load_preferences, models, recipients as get_recipients
from fmn.tests import Base as BaseTestCase


@mock.patch('fmn.lib.fmn_config.app_conf', {'fmn.backends': ['post', 'pidgeon']})
class LoadPreferenceTests(BaseTestCase):

    def setUp(self):
        super(LoadPreferenceTests, self).setUp()
        user = models.User(openid='jcline', openid_url='http://jcline.id.fedoraproject.org/')
        user2 = models.User(
            openid='bowlofeggs', openid_url='http://bowlofeggs.id.fedoraproject.org/')
        context = models.Context(name='pidgeon', description='A bird', detail_name='Bird', icon='?')
        context2 = models.Context(
            name='post', description='Old school', detail_name='The Post', icon='?')
        pref = models.Preference(openid='jcline', enabled=True, context_name='pidgeon')
        pref2 = models.Preference(openid='jcline', enabled=False, context_name='post')
        pref3 = models.Preference(openid='bowlofeggs', enabled=False, context_name='post')
        for obj in (user, user2, context, context2, pref, pref2, pref3):
            self.sess.add(obj)
        self.sess.commit()

    def test_load_all_preferences(self):
        """Assert all preferences including disabled are loaded by default"""
        preferences = load_preferences()
        self.assertEqual(3, len(preferences))

        for key in ('jcline_pidgeon', 'jcline_post', 'bowlofeggs_post'):
            self.assertTrue(key in preferences)
            openid, context = key.split('_')
            pref = models.Preference.query.filter(
                models.Preference.openid == openid,
                models.Preference.context_name == context).first()
            self.assertEqual(pref.__json__(reify=True), preferences[key])

    def test_load_preferences_cull_backends(self):
        """Assert all preferences are loaded, excepting specified backends"""
        preferences = load_preferences(cull_backends=['pidgeon'])
        self.assertEqual(2, len(preferences))

        for key in ('jcline_post', 'bowlofeggs_post'):
            self.assertTrue(key in preferences)
            openid, context = key.split('_')
            pref = models.Preference.query.filter(
                models.Preference.openid == openid,
                models.Preference.context_name == context).first()
            self.assertEqual(pref.__json__(reify=True), preferences[key])

    def test_load_preferences_skip_disabled(self):
        """Assert all preferences are loaded, excepting disabled preferences"""
        preferences = load_preferences(cull_disabled=True)
        self.assertEqual(1, len(preferences))

        pref = models.Preference.query.filter(
            models.Preference.openid == 'jcline',
            models.Preference.context_name == 'pidgeon').first()
        self.assertEqual(pref.__json__(reify=True), preferences['jcline_pidgeon'])


class TestRecipients(BaseTestCase):

    def create_user_and_context_data(self):
        models.User.get_or_create(
            self.sess, openid="ralph.id.fedoraproject.org",
            openid_url="http://ralph.id.fedoraproject.org/",
        )
        models.User.get_or_create(
            self.sess, openid="toshio.id.fedoraproject.org",
            openid_url="http://toshio.id.fedoraproject.org/",
        )
        models.Context.create(
            self.sess, name="irc", description="Internet Relay Chat",
            detail_name="irc nick", icon="user",
        )
        models.Context.create(
            self.sess, name="android", description="Google Cloud Messaging",
            detail_name="registration id", icon="phone",
        )

    def create_preference_data_empty(self):
        user = models.User.get(
            self.sess, openid="ralph.id.fedoraproject.org")
        context = models.Context.get(self.sess, name="irc")
        preference = models.Preference.create(
            self.sess,
            user=user,
            context=context,
            detail_value="threebean",
        )
        preference.enabled = False

        user = models.User.get(
            self.sess, openid="toshio.id.fedoraproject.org")
        context = models.Context.get(self.sess, name="irc")
        preference = models.Preference.create(
            self.sess,
            user=user,
            context=context,
            detail_value="abadger1999",
        )

    def create_preference_data_basic(self, code_path):
        user = models.User.get(
            self.sess, openid="ralph.id.fedoraproject.org")
        context = models.Context.get(self.sess, name="irc")
        preference = models.Preference.load(self.sess, user, context)
        filter = models.Filter.create(self.sess, name="test filter")
        filter.add_rule(self.sess, self.valid_paths, code_path)
        preference.add_filter(self.sess, filter)

        user = models.User.get(
            self.sess, openid="toshio.id.fedoraproject.org")
        context = models.Context.get(self.sess, name="irc")
        preference = models.Preference.load(self.sess, user, context)
        filter = models.Filter.create(self.sess, name="test filter 2")
        filter.add_rule(self.sess, self.valid_paths, code_path)
        preference.add_filter(self.sess, filter)

    def test_empty_recipients_list(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()

        msg = {
            "wat": "blah",
        }
        preferences = load_preferences()
        recipients = get_recipients(
            preferences, msg, self.valid_paths, self.config)
        self.assertEqual(recipients, {})

    def test_basic_recipients_list(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()
        expected_recipients = [
            {
                'triggered_by_links': True,
                'markup_messages': False,
                'shorten_links': False,
                'irc nick': 'threebean',
                'user': 'ralph.id.fedoraproject.org',
                'filter_name': 'test filter',
                'filter_id': 1,
                'filter_oneshot': False,
                'verbose': True,
            },
            {
                'triggered_by_links': True,
                'markup_messages': False,
                'shorten_links': False,
                'irc nick': 'abadger1999',
                'user': 'toshio.id.fedoraproject.org',
                'filter_name': 'test filter 2',
                'filter_id': 2,
                'filter_oneshot': False,
                'verbose': True,
            },
        ]

        code_path = "fmn.tests.example_rules:wat_rule"
        self.create_preference_data_basic(code_path)

        msg = {
            "wat": "blah",
        }
        preferences = load_preferences()
        recipients = get_recipients(
            preferences, msg, self.valid_paths, self.config)
        self.assertEqual(expected_recipients, recipients['irc'])

    def test_miss_recipients_list(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()

        code_path = "fmn.tests.example_rules:not_wat_rule"
        self.create_preference_data_basic(code_path)

        msg = {
            "wat": "blah",
        }
        preferences = load_preferences()
        recipients = get_recipients(
            preferences, msg, self.valid_paths, self.config)
        self.assertEqual(recipients, {})

    def test_multiple_identical_filters_miss(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()

        # Tack two identical filters onto the preferenced
        code_path = "fmn.tests.example_rules:not_wat_rule"
        self.create_preference_data_basic(code_path)
        code_path = "fmn.tests.example_rules:not_wat_rule"
        self.create_preference_data_basic(code_path)

        preference = models.Preference.load(
            self.sess, "ralph.id.fedoraproject.org", "irc")
        self.assertEqual(len(preference.filters), 2)

        msg = {
            "wat": "blah",
        }
        preferences = load_preferences()
        recipients = get_recipients(
            preferences, msg, self.valid_paths, self.config)
        self.assertEqual(recipients, {})

    def test_multiple_identical_filters_hit(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()

        # Tack two identical filters onto the preferenced
        code_path = "fmn.tests.example_rules:wat_rule"
        self.create_preference_data_basic(code_path)
        code_path = "fmn.tests.example_rules:wat_rule"
        self.create_preference_data_basic(code_path)

        preference = models.Preference.load(
            self.sess, "ralph.id.fedoraproject.org", "irc")
        self.assertEqual(len(preference.filters), 2)

        msg = {
            "wat": "blah",
        }
        preferences = load_preferences()
        recipients = get_recipients(
            preferences, msg, self.valid_paths, self.config)
        expected_recipients = [
            {
                'triggered_by_links': True,
                'markup_messages': False,
                'shorten_links': False,
                'irc nick': 'threebean',
                'user': 'ralph.id.fedoraproject.org',
                'filter_name': 'test filter',
                'filter_id': 1,
                'filter_oneshot': False,
                'verbose': True,
            },
            {
                'triggered_by_links': True,
                'markup_messages': False,
                'shorten_links': False,
                'irc nick': 'abadger1999',
                'user': 'toshio.id.fedoraproject.org',
                'filter_name': 'test filter 2',
                'filter_id': 2,
                'filter_oneshot': False,
                'verbose': True,
            },
        ]
        self.assertEqual(expected_recipients, recipients['irc'])

    def test_multiple_different_filters_hit(self):
        self.create_user_and_context_data()
        self.create_preference_data_empty()

        # Tack two identical filters onto the preferenced
        code_path = "fmn.tests.example_rules:wat_rule"
        self.create_preference_data_basic(code_path)
        code_path = "fmn.tests.example_rules:not_wat_rule"
        self.create_preference_data_basic(code_path)

        preference = models.Preference.load(
            self.sess, "ralph.id.fedoraproject.org", "irc")
        self.assertEqual(len(preference.filters), 2)

        msg = {
            "wat": "blah",
        }
        preferences = load_preferences()
        recipients = get_recipients(
            preferences, msg, self.valid_paths, self.config)
        expected_recipients = [
            {
                'triggered_by_links': True,
                'markup_messages': False,
                'shorten_links': False,
                'irc nick': 'threebean',
                'user': 'ralph.id.fedoraproject.org',
                'filter_name': 'test filter',
                'filter_id': 1,
                'filter_oneshot': False,
                'verbose': True,
            },
            {
                'triggered_by_links': True,
                'markup_messages': False,
                'shorten_links': False,
                'irc nick': 'abadger1999',
                'user': 'toshio.id.fedoraproject.org',
                'filter_name': 'test filter 2',
                'filter_id': 2,
                'filter_oneshot': False,
                'verbose': True,
            },
        ]
        self.assertEqual(expected_recipients, recipients['irc'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
