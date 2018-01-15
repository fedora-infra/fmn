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

import datetime

from dogpile import cache
from kombu import Queue
import mock
import sqlalchemy

from fmn import tasks, lib as fmn_lib, constants
from fmn.exceptions import FmnError
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

    @mock.patch.dict('fmn.tasks.config.app_conf', {'fmn.backends': ['sse']})
    @mock.patch('fmn.tasks.formatters.sse')
    @mock.patch('fmn.rules.utils._cache', new_callable=cache.make_region)
    @mock.patch('fmn.tasks.connections')
    def test_run_recipients_found(self, mock_conns, mock_rules_cache, mock_fmt_sse):
        """Assert messages are sent to the backend when recipients are found."""
        mock_fmt_sse.return_value = 'Such pretty, very message'
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
            'recipient': {
                'triggered_by_links': True,
                'markup_messages': False,
                'user': u'jcline.id.fedoraproject.org',
                'filter_name': u'Events referring to my username',
                u'SSE': u'jcline',
                'filter_oneshot': False,
                'filter_id': 2,
                'shorten_links': False,
                'verbose': True
            },
            'fedmsg': message,
            'formatted_message': 'Such pretty, very message'
        }

        find_recipients.run(message)
        conn = mock_conns.__getitem__.return_value.acquire.return_value.__enter__.return_value
        conn.Producer.return_value.publish.assert_called_with(
            expected_published_message,
            routing_key=constants.BACKEND_QUEUE_PREFIX + 'sse',
            declare=[Queue(constants.BACKEND_QUEUE_PREFIX + 'sse', durable=True)],
        )


class BatchReadyTests(Base):
    """Tests for the :func:`fmn.tasks._batch_ready` function."""

    def setUp(self):
        super(BatchReadyTests, self).setUp()
        # Set up a user with preferences to match the message
        self.user = models.User(
            openid='jcline.id.fedoraproject.org', openid_url='http://jcline.id.fedoraproject.org')
        self.sess.add(self.user)
        self.context = models.Context(
            name='sse', description='description', detail_name='SSE', icon='wat')
        self.sess.add(self.context)
        self.sess.commit()
        fmn_lib.defaults.create_defaults_for(self.sess, self.user, detail_values={'sse': 'jcline'})
        self.sess.commit()
        self.preference = models.Preference.query.filter_by(
            context_name='sse', openid='jcline.id.fedoraproject.org').first()
        self.preference.enabled = True
        self.sess.add(self.preference)
        self.sess.commit()

    def test_no_messages(self):
        """Assert when there aren't any messages, there's not a batch ready for a user."""
        self.assertFalse(tasks._batch_ready(self.preference))

    def test_by_count(self):
        """Assert when at least as many messages queued as the batch count, a batch is ready."""
        self.preference.batch_count = 1
        message = models.QueuedMessage(user=self.user, context=self.context)
        message.message = {}
        self.sess.add(message)
        self.sess.commit()

        self.assertTrue(tasks._batch_ready(self.preference))

    def test_by_time(self):
        """
        Assert that when the earliest message was delivered "batch_delta" seconds ago, a
        batch is ready.
        """
        self.preference.batch_delta = 60 * 60
        message = models.QueuedMessage(
            user=self.user, context=self.context, created_on=datetime.datetime(2010, 1, 1))
        message.message = {}
        self.sess.add(message)
        self.sess.commit()

        self.assertTrue(tasks._batch_ready(self.preference))

    def test_not_ready(self):
        """Assert when there are messages, but the count and time aren't met, there's no batch."""
        self.preference.batch_delta = 60 * 60
        message = models.QueuedMessage(user=self.user, context=self.context)
        message.message = {}
        self.sess.add(message)
        self.sess.commit()

        self.assertFalse(tasks._batch_ready(self.preference))


@mock.patch('fmn.tasks.connections')
class ConfirmationsTests(Base):
    """Tests for the :func:`fmn.tasks.confirmations` function."""

    def test_email_pending(self, mock_conns):
        """Assert the expected message is dispatched for pending email confirmation."""
        user = models.User(
            openid='jcline.id.fedoraproject.org', openid_url='http://jcline.id.fedoraproject.org')
        context = models.Context(
            name='email', description='description', detail_name='email', icon='wat')
        confirmation = models.Confirmation(
            secret='a'*32, detail_value='jeremy@jcline.org', user=user, context=context)
        self.sess.add(confirmation)
        self.sess.commit()
        expected_email = """Precedence: Bulk
Auto-Submitted: auto-generated
From: notifications@fedoraproject.org
To: jeremy@jcline.org
Subject: Confirm notification email

jcline.id.fedoraproject.org has requested that notifications be sent to this email address
* To accept, visit this address:
  http://localhost:5000/confirm/accept/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
* Or, to reject you can visit this address:
  http://localhost:5000/confirm/reject/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Alternatively, you can ignore this.  This is an automated message, please
email notifications@fedoraproject.org if you have any concerns/issues/abuse."""
        expected_message = {
            'context': 'email',
            'recipient': {
                'email': 'jeremy@jcline.org',
                'user': 'jcline.id.fedoraproject.org',
                'triggered_by_links': False,
                'confirmation': True,
            },
            'fedmsg': {},
            'formatted_message': expected_email,
        }

        tasks.confirmations()

        conn = mock_conns.__getitem__.return_value.acquire.return_value.__enter__.return_value
        self.assertEqual(
            expected_message, conn.Producer.return_value.publish.call_args_list[0][0][0])

    def test_irc_pending(self, mock_conns):
        """Assert the expected message is dispatched for pending irc nick confirmation."""
        user = models.User(
            openid='jcline.id.fedoraproject.org', openid_url='http://jcline.id.fedoraproject.org')
        context = models.Context(
            name='irc', description='description', detail_name='irc nick', icon='wat')
        confirmation = models.Confirmation(
            secret='a'*32, detail_value='jcline', user=user, context=context)
        self.sess.add(confirmation)
        self.sess.commit()
        expected_message = {
            'context': 'irc',
            'recipient': {
                'irc nick': 'jcline',
                'user': 'jcline.id.fedoraproject.org',
                'triggered_by_links': False,
                'confirmation': True,
            },
            'fedmsg': {},
            'formatted_message': u'',  # right now the backend still formats the message
        }

        tasks.confirmations()

        conn = mock_conns.__getitem__.return_value.acquire.return_value.__enter__.return_value
        self.assertEqual(
            expected_message, conn.Producer.return_value.publish.call_args_list[0][0][0])

    def test_expired_reaped(self, mock_conns):
        """Assert confirmations that have expired are deleted and not sent."""
        user = models.User(
            openid='jcline.id.fedoraproject.org', openid_url='http://jcline.id.fedoraproject.org')
        context = models.Context(
            name='irc', description='description', detail_name='irc nick', icon='wat')
        created = datetime.datetime.utcnow() - datetime.timedelta(days=2)
        confirmation = models.Confirmation(
            created_on=created, secret='a'*32, detail_value='jcline', user=user, context=context)
        self.sess.add(confirmation)
        self.sess.commit()

        tasks.confirmations()

        conn = mock_conns.__getitem__.return_value.acquire.return_value.__enter__.return_value
        self.assertEqual(0, conn.Producer.return_value.publish.call_count)

    def test_handled_valid(self, mock_conns):
        """
        Assert confirmation is placed in the 'valid' state until a backend marks it
        otherwise.
        """
        user = models.User(
            openid='jcline.id.fedoraproject.org', openid_url='http://jcline.id.fedoraproject.org')
        context = models.Context(
            name='irc', description='description', detail_name='irc nick', icon='wat')
        confirmation = models.Confirmation(
            secret='a'*32, detail_value='jcline', user=user, context=context)
        self.sess.add(confirmation)
        self.sess.commit()

        tasks.confirmations()

        confirmation = models.Confirmation.query.all()
        self.assertEqual(1, len(confirmation))
        self.assertEqual('valid', confirmation[0].status)


@mock.patch('fmn.tasks.formatters')
class FormatTests(Base):

    def setUp(self):
        super(FormatTests, self).setUp()
        self.message = {
            'body': {
                "msg": {
                    "changed": "rules",
                    "context": "email",
                    "openid": "jcline.id.fedoraproject.org"
                },
                "msg_id": "2017-6aa71d5b-fbe4-49e7-afdd-afcf0d22802b",
                "timestamp": 1507310730,
                "topic": "org.fedoraproject.dev.fmn.filter.update",
                "username": "vagrant",
            }
        }
        self.recipient = {
            "email address": "jeremy@jcline.org",
            "filter_id": 11,
            "filter_name": "test",
            "filter_oneshot": False,
            "markup_messages": False,
            "shorten_links": False,
            "triggered_by_links": False,
            "user": "jcline.id.fedoraproject.org",
            "verbose": True,
        }

    def test_failure(self, mock_formatters):
        """Assert an exception is raised if there's no formatted message."""
        mock_formatters.email.return_value = None
        self.assertRaises(FmnError, tasks._format, 'email', self.message, self.recipient)

        mock_formatters.email.assert_called_once_with(self.message['body'], self.recipient)

    def test_single_email(self, mock_formatters):
        """Assert single messages for email context use the correct formatter."""
        tasks._format('email', self.message, self.recipient)

        mock_formatters.email.assert_called_once_with(self.message['body'], self.recipient)

    def test_multi_email(self, mock_formatters):
        """Assert multiple messages for email context use the correct formatter."""
        tasks._format('email', [self.message, self.message], self.recipient)

        mock_formatters.email_batch.assert_called_once_with(
            [self.message['body'], self.message['body']], self.recipient)

    def test_single_irc(self, mock_formatters):
        """Assert single messages for irc context use the correct formatter."""
        tasks._format('irc', self.message, self.recipient)

        mock_formatters.irc.assert_called_once_with(self.message['body'], self.recipient)

    def test_multi_irc(self, mock_formatters):
        """Assert multiple messages for irc context use the correct formatter."""
        tasks._format('irc', [self.message, self.message], self.recipient)

        mock_formatters.irc_batch.assert_called_once_with(
            [self.message['body'], self.message['body']], self.recipient)


class MaybeMarkFilterFiredTests(Base):
    """Tests for :func:`tasks._maybe_mark_filter_fired`."""

    def test_no_filter_oneshot(self):
        """Assert if the filter_oneshot key is missing, None is returned."""
        self.assertTrue(tasks._maybe_mark_filter_fired({}) is None)

    def test_filter_oneshot_false(self):
        """Assert if the filter_oneshot key is missing, None is returned."""
        self.assertTrue(tasks._maybe_mark_filter_fired({'filter_oneshot': False}) is None)

    @mock.patch('fmn.tasks._log')
    def test_invalid_filter_id(self, mock_log):
        """Assert if the filter_id references an invalid key, nothing bad happens."""
        recipient = {'filter_oneshot': True, 'filter_id': 8675309}

        self.assertTrue(tasks._maybe_mark_filter_fired(recipient) is None)
        mock_log.exception.assert_called_once_with(
            'Unable to mark one-shot filter (id %s) as fired', 8675309)

    def test_valid_oneshot_filter(self):
        """Assert oneshot filters are properly deactivated."""
        session = models.Session()
        filt = models.Filter(active=True, oneshot=True)
        session.add(filt)
        session.commit()
        recipient = {'filter_oneshot': True, 'filter_id': filt.id}

        self.assertTrue(tasks._maybe_mark_filter_fired(recipient) is None)
        self.assertEqual(1, models.Filter.query.count())
        self.assertFalse(models.Filter.query.one().active)


class BatchTests(Base):
    """Tests for :func:`tasks._batch`."""

    def setUp(self):
        super(BatchTests, self).setUp()
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

        self. message = {
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

        self.recipient = {
            'triggered_by_links': True,
            'markup_messages': False,
            'user': u'jcline.id.fedoraproject.org',
            'filter_name': u'Events referring to my username',
            u'SSE': u'jcline',
            'filter_oneshot': False,
            'filter_id': 2,
            'shorten_links': False,
            'verbose': True
        }

    def test_no_batch_delta_or_count(self):
        """Assert False is returned if the message isn't batched."""
        self.assertFalse(tasks._batch({}, 'sse', self.recipient, self.message))

    def test_batch_count(self):
        """Assert the batch_count keyword triggers batching."""
        self.assertTrue(tasks._batch({'batch_count': True}, 'sse', self.recipient, self.message))
        self.assertEqual(1, models.QueuedMessage.query.count())

    def test_batch_delta(self):
        """Assert the batch_delta keyword triggers batching."""
        self.assertTrue(tasks._batch({'batch_delta': True}, 'sse', self.recipient, self.message))
        self.assertEqual(1, models.QueuedMessage.query.count())

    @mock.patch('fmn.tasks.models.QueuedMessage.enqueue')
    def test_batch_failure(self, mock_enqueue):
        """Assert a database failure results in the message not being queued."""
        mock_enqueue.side_effect = sqlalchemy.exc.SQLAlchemyError('boop')

        self.assertFalse(tasks._batch({'batch_delta': True}, 'sse', self.recipient, self.message))
        self.assertEqual(0, models.QueuedMessage.query.count())
