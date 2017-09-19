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
"""Tests for the :mod:`fmn.tasks` module."""

from dogpile import cache
from kombu import Queue
import mock

from fmn import tasks, lib as fmn_lib
from fmn.lib import models
from fmn.tests import Base


class FindRecipientsTestCase(Base):

    def test_valid_paths(self):
        """Assert the valid paths is lazy-loaded on attribute access."""
        find_recipients = tasks._FindRecipients()

        self.assertTrue(find_recipients._valid_paths is None)
        self.assertEqual(fmn_lib.load_rules(root="fmn.rules"), find_recipients.valid_paths)
        self.assertTrue(find_recipients._valid_paths is find_recipients.valid_paths)

    def test_user_preferences(self):
        """Assert the user preferences are lazy-loaded on attribute access."""
        find_recipients = tasks._FindRecipients()
        expected_preferences = fmn_lib.load_preferences(
            cull_disabled=True, cull_backends=['desktop'])

        self.assertTrue(find_recipients._user_preferences is None)
        self.assertEqual(expected_preferences, find_recipients.user_preferences)
        self.assertTrue(find_recipients._user_preferences is find_recipients.user_preferences)

    @mock.patch('fmn.lib.update_preferences')
    def test_run_fmn_message(self, mock_update_prefs):
        """Assert messages with .fmn. in the topic cause preferences to be refreshed."""
        find_recipients = tasks._FindRecipients()
        message = {
            'topic': 'fmn.internal.refresh_cache',
            'body': 'jcline.id.fedoraproject.org',
        }

        find_recipients.run(message)
        mock_update_prefs.assert_called_once_with(
            'jcline.id.fedoraproject.org', find_recipients.user_preferences)

    @mock.patch('fmn.tasks.connections')
    def test_run_no_recipients(self, mock_conns):
        """Assert messages without any recipients results in no messages to the backend."""
        find_recipients = tasks._FindRecipients()
        user = models.User(
            openid='jcline.id.fedoraproject.org', openid_url='http://jcline.id.fedoraproject.org')
        fmn_lib.defaults.create_defaults_for(self.sess, user)
        self.sess.commit()
        message = {
            'topic': 'com.example.fmn.message',
            'body': {
                'msg': {'openid': 'jcline.id.fedoraproject.org'}
            }
        }

        find_recipients.run(message)

        conn = mock_conns.__getitem__.return_value.acquire.return_value.__enter__.return_value
        self.assertEqual(0, conn.Producer.return_value.publish.call_count)

    @mock.patch('fmn.rules.utils._cache', new_callable=cache.make_region)
    @mock.patch('fmn.tasks.connections')
    def test_run_recipients_found(self, mock_conns, mock_rules_cache):
        """Assert messages are sent to the backend when recipients are found."""
        find_recipients = tasks._FindRecipients()

        mock_rules_cache.configure(backend='dogpile.cache.memory')

        # Set up a user with preferences to match the message
        user = models.User(
            openid='jcline.id.fedoraproject.org', openid_url='http://jcline.id.fedoraproject.org')
        self.sess.add(user)
        context = models.Context(
            name='sse', description='description', detail_name='SSE', icon='wat')
        self.sess.add(context)
        self.sess.commit()
        fmn_lib.defaults.create_defaults_for(self.sess, user, detail_values={'sse': 'jcline'})
        self.sess.commit()
        preference = models.Preference.query.filter_by(
            context_name='sse', openid='jcline.id.fedoraproject.org').first()
        preference.enabled = True
        self.sess.add(preference)
        self.sess.commit()

        message = {
            "topic": "org.fedoraproject.prod.buildsys.build.state.change",
            'body': {
                "username": "apache",
                "i": 1,
                "timestamp": 1505399391.0,
                "msg_id": "2017-7c65d9ff-85c0-42bb-8288-9b6112cb3da2",
                "topic": "org.fedoraproject.prod.buildsys.build.state.change",
                "msg": {
                    "build_id": 970796,
                    "old": 0,
                    "name": "fedmsg",
                    "task_id": 21861152,
                    "attribute": "state",
                    "request": [
                        ("git://pkgs.fedoraproject.org/rpms/fedmsg?#"
                         "870987e84539239a22170475bbf13ac4d2ef4382"),
                        "f26-candidate",
                        {},
                    ],
                    "instance": "primary",
                    "version": "1.0.1",
                    "owner": "jcline",
                    "new": 1,
                    "release": "4.fc26"
                }
            }
        }

        expected_published_message = {
            'context': u'sse',
            'recipients': [{
                'triggered_by_links': True,
                'markup_messages': False,
                'user': u'jcline.id.fedoraproject.org',
                'filter_name': u'Events referring to my username',
                u'SSE': u'jcline',
                'filter_oneshot': False,
                'filter_id': 2,
                'shorten_links': False,
                'verbose': True
            }],
            'raw_msg': message,
        }

        find_recipients.run(message)
        conn = mock_conns.__getitem__.return_value.acquire.return_value.__enter__.return_value
        conn.Producer.return_value.publish.assert_called_with(
            expected_published_message,
            routing_key='backends',
            declare=[Queue('backends', durable=True)],
        )
