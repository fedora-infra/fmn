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
"""Unit tests for the :mod:`fmn.formatters` module."""

import json

import fedmsg.meta
import mock
import requests

from . import Base
from fmn import formatters
from fmn.lib import models


class ShortenTests(Base):
    """Tests for :func:`fmn.formatters.shorten`."""

    def test_no_link(self):
        """Assert an empty string is returned when no link is provided."""
        self.assertEqual('', formatters.shorten(None))

    @mock.patch('fmn.formatters.requests.get')
    def test_failed_request(self, mock_get):
        """Assert a failed request results in the original link."""
        mock_get.side_effect = requests.exceptions.RequestException()

        self.assertEqual('original link', formatters.shorten('original link'))

    @mock.patch('fmn.formatters.requests.get')
    def test_success(self, mock_get):
        mock_get.return_value.text = '\n http://so.short/abc \n'
        shortened_link = formatters.shorten('http://www.example.com/')

        self.assertEqual('http://so.short/abc', shortened_link)


class IrcTests(Base):
    """Tests for :func:`fmn.formatters.irc`."""
    def setUp(self):
        super(IrcTests, self).setUp()
        fedmsg.meta.make_processors(**self.config)
        self.message = {
            u'username': u'apache',
            u'i': 1,
            u'timestamp': 1478281861,
            u'msg_id': u'2016-c2184569-f9c4-4c52-affd-79e28848d70f',
            u'crypto': u'x509',
            u'topic': u'org.fedoraproject.prod.buildsys.task.state.change',
            u'msg': {
                u'info': {
                    u'children': [],
                    u'parent': None,
                    u'channel_id': 1,
                    u'start_time': u'2016-11-04 17:51:01.254871',
                    u'request': [
                        u'../packages/eclipse/4.5.0/1.fc26/src/eclipse-4.5.0-1.fc26.src.rpm',
                        u'f26',
                        {u'scratch': True, u'arch_override': u'x86_64'}
                    ],
                    u'state': 1,
                    u'awaited': None,
                    u'method': u'build',
                    u'priority': 50,
                    u'completion_time': None,
                    u'waiting': None,
                    u'create_time': u'2016-11-04 17:50:57.825631',
                    u'owner': 3199,
                    u'host_id': 82,
                    u'label': None,
                    u'arch': u'noarch',
                    u'id': 16289846
                },
                u'old': u'FREE',
                u'attribute': u'state',
                u'method': u'build',
                u'instance': u'primary',
                u'owner': u'koschei',
                u'new': u'OPEN',
                u'srpm': u'eclipse-4.5.0-1.fc26.src.rpm',
                u'id': 16289846
            }
        }
        self.recipient = {
            "triggered_by_links": False,
            "markup_messages": False,
            "user": "jcline.id.fedoraproject.org",
            "filter_name": "firehose",
            "filter_oneshot": True,
            "filter_id": 7,
            "shorten_links": False,
            "verbose": True,
        }

    def test_confirmation(self):
        """Assert the IRC confirmation message is formatted as expected."""
        confirmation = models.Confirmation(
            secret='a'*32,
            detail_value='jeremy@jcline.org',
            openid='jcline.id.fedoraproject.org',
            context_name='email',
        )
        expected = u"""
jcline.id.fedoraproject.org has requested that notifications be sent to this nick
* To accept, visit this address:
  http://localhost:5000/confirm/accept/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
* Or, to reject you can visit this address:
  http://localhost:5000/confirm/reject/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Alternatively, you can ignore this.  This is an automated message, please
email notifications@fedoraproject.org if you have any concerns/issues/abuse.
I am run by Fedora Infrastructure.  Type 'help' for more information.
"""

        message = formatters.irc_confirmation(confirmation)

        self.assertEqual(expected.strip(), message)

    @mock.patch('fmn.formatters.arrow.get')
    def test_format_unmarked(self, mock_arrow):
        mock_arrow.return_value.humanize.return_value = '2 months ago'
        expected_message = (
            u'koschei\'s scratch build of eclipse-4.5.0-1.fc26.src.rpm for f26 started 2 months'
            u' ago http://koji.fedoraproject.org/koji/taskinfo?taskID=16289846'
        )
        formatted_message = formatters.irc(self.message, self.recipient)
        self.assertEqual(expected_message, formatted_message)

    @mock.patch('fmn.formatters.arrow.get')
    def test_format_marked_up(self, mock_arrow):
        """Assert pretty colors are added to IRC messages if marked up."""
        mock_arrow.return_value.humanize.return_value = '2 score and 3 days ago'
        self.recipient['markup_messages'] = True
        expected_message = (
            u"\x038buildsys.task.state.change\x03 -- koschei's scratch build of "
            u"eclipse-4.5.0-1.fc26.src.rpm for f26 started 2 score and 3 days ago"
            u" \x0310http://koji.fedoraproject.org/koji/taskinfo?taskID=16289846\x03"
        )

        formatted_message = formatters.irc(self.message, self.recipient)
        self.assertEqual(expected_message, formatted_message)

    @mock.patch('fmn.formatters.arrow.get')
    def test_format_triggered_by(self, mock_arrow):
        """Assert triggered-by links are added to IRC messages if configured to."""
        mock_arrow.return_value.humanize.return_value = 'eleventy-one minutes ago'
        self.recipient['triggered_by_links'] = True
        expected_message = (
            u"koschei's scratch build of eclipse-4.5.0-1.fc26.src.rpm for f26 started "
            u"eleventy-one minutes ago http://koji.fedoraproject.org/koji/taskinfo?taskID=16289846"
            u" (triggered by http://localhost:5000/jcline.id.fedoraproject.org/irc/7)"
        )

        formatted_message = formatters.irc(self.message, self.recipient)
        self.assertEqual(expected_message, formatted_message)

    @mock.patch('fmn.formatters.arrow.get')
    def test_shorten(self, mock_arrow):
        """Assert links are shortened."""
        mock_arrow.return_value.humanize.return_value = 'Schfourteenteen hours ago'
        self.recipient['shorten_links'] = True
        self.recipient['triggered_by_links'] = True

        expected_message = (
            u'koschei\'s scratch build of eclipse-4.5.0-1.fc26.src.rpm for f26 started '
            u'Schfourteenteen hours ago https://da.gd/TT0da (triggered by https://da.gd/B800F)'
        )

        formatted_message = formatters.irc(self.message, self.recipient)
        self.assertEqual(expected_message, formatted_message)


class SseTests(Base):

    def setUp(self):
        super(SseTests, self).setUp()
        fedmsg.meta.make_processors(**self.config)

    def test_format_message_conglomerated(self):
        """Assert conglomerated messages are formatted"""
        message = {
            u'subtitle': u'relrod pushed commits to ghc and 487 other packages',
            u'link': u'http://example.com/',
            u'icon': u'https://that-git-logo',
            u'secondary_icon': u'https://that-relrod-avatar',
            u'start_time': 0,
            u'end_time': 100,
            u'human_time': u'5 minutes ago',
            u'usernames': [u'relrod'],
            u'packages': [u'ghc', u'nethack'],
            u'topics': [u'org.fedoraproject.prod.git.receive'],
            u'categories': [u'git'],
            u'msg_ids': {
                u'2014-abcde': {
                    u'subtitle': u'relrod pushed some commits to ghc',
                    u'title': u'git.receive',
                    u'link': u'http://...',
                    u'icon': u'http://...',
                },
                u'2014-bcdef': {
                    u'subtitle': u'relrod pushed some commits to nethack',
                    u'title': u'git.receive',
                    u'link': u'http://...',
                    u'icon': u'http://...',
                },
            },
        }
        recipient = {
            "triggered_by_links": True,
            "markup_messages": True,
            "user": "jcline.id.fedoraproject.org",
            "filter_name": "firehose",
            "filter_oneshot": True,
            "filter_id": 7,
            "shorten_links": False,
            "verbose": True,
        }

        formatted_message = formatters.sse(message, recipient)
        formatted_message = json.loads(formatted_message)
        for key in ('dom_id', 'date_time', 'icon', 'link', 'markup', 'secondary_icon'):
            self.assertTrue(key in formatted_message)

    def test_format_message_raw(self):
        """Assert raw messages are formatted"""
        message = {
            u'username': u'apache',
            u'i': 1,
            u'timestamp': 1478281861,
            u'msg_id': u'2016-c2184569-f9c4-4c52-affd-79e28848d70f',
            u'crypto': u'x509',
            u'topic': u'org.fedoraproject.prod.buildsys.task.state.change',
            u'msg': {
                u'info': {
                    u'children': [],
                    u'parent': None,
                    u'channel_id': 1,
                    u'start_time': u'2016-11-04 17:51:01.254871',
                    u'request': [
                        u'../packages/eclipse/4.5.0/1.fc26/src/eclipse-4.5.0-1.fc26.src.rpm',
                        u'f26',
                        {u'scratch': True, u'arch_override': u'x86_64'}
                    ],
                    u'state': 1,
                    u'awaited': None,
                    u'method': u'build',
                    u'priority': 50,
                    u'completion_time': None,
                    u'waiting': None,
                    u'create_time': u'2016-11-04 17:50:57.825631',
                    u'owner': 3199,
                    u'host_id': 82,
                    u'label': None,
                    u'arch': u'noarch',
                    u'id': 16289846
                },
                u'old': u'FREE',
                u'attribute': u'state',
                u'method': u'build',
                u'instance': u'primary',
                u'owner': u'koschei',
                u'new': u'OPEN',
                u'srpm': u'eclipse-4.5.0-1.fc26.src.rpm',
                u'id': 16289846
            }
        }
        recipient = {
            "triggered_by_links": True,
            "markup_messages": True,
            "user": "jcline.id.fedoraproject.org",
            "filter_name": "firehose",
            "filter_oneshot": True,
            "filter_id": 7,
            "shorten_links": False,
            "verbose": True,
        }

        formatted_message = formatters.sse(message, recipient)
        formatted_message = json.loads(formatted_message)
        for key in ('dom_id', 'date_time', 'icon', 'link', 'markup', 'secondary_icon'):
            self.assertTrue(key in formatted_message)


class EmailTests(Base):

    def setUp(self):
        super(EmailTests, self).setUp()
        self.message = {
            "msg": {
                "changed": "rules",
                "context": "email",
                "openid": "jcline.id.fedoraproject.org"
            },
            "msg_id": "2017-6aa71d5b-fbe4-49e7-afdd-afcf0d22802b",
            "timestamp": 1507310730,
            "topic": "org.fedoraproject.dev.fmn.filter.update",
            "username": "vagrant"
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

    def test_base_email(self):
        """Assert the basic email has the auto-generation headers."""
        message = formatters._base_email()

        self.assertEqual(message['Auto-Submitted'], 'auto-generated')
        self.assertEqual(message['Precedence'], 'Bulk')
        self.assertEqual(message['From'], 'notifications@fedoraproject.org')

    def test_confirmation(self):
        """Assert a :class:`models.Confirmation` is formatted to an email."""
        confirmation = models.Confirmation(
            secret='a'*32,
            detail_value='jeremy@jcline.org',
            openid='jcline.id.fedoraproject.org',
            context_name='email',
        )
        expected = """Precedence: Bulk
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

        message = formatters.email_confirmation(confirmation)

        self.assertEqual(expected, message)

    def test_email(self):
        """Assert a well-formed email is returned from a basic message."""
        expected = (
            'Precedence: Bulk\n'
            'Auto-Submitted: auto-generated\n'
            'From: notifications@fedoraproject.org\n'
            'To: jeremy@jcline.org\n'
            'X-Fedmsg-Topic: org.fedoraproject.dev.fmn.filter.update\n'
            'X-Fedmsg-Category: fmn\n'
            'X-Fedmsg-Username: jcline\n'
            'X-Fedmsg-Num-Packages: 0\n'
            'Subject: jcline updated the rules on a fmn email filter\n'
            'MIME-Version: 1.0\n'
            'Content-Type: text/plain; charset="utf-8"\n'
            'Content-Transfer-Encoding: base64\n\n'
            'Tm90aWZpY2F0aW9uIHRpbWUgc3RhbXBlZCAyMDE3LTEwLTA2IDE3OjI1OjMwIFVUQwoKamNsaW5l\n'
            'IHVwZGF0ZWQgdGhlIHJ1bGVzIG9uIGEgZm1uIGVtYWlsIGZpbHRlcgoJaHR0cHM6Ly9hcHBzLmZl\n'
            'ZG9yYXByb2plY3Qub3JnL25vdGlmaWNhdGlvbnMv\n'
        )

        actual = formatters.email(self.message, self.recipient)
        self.assertEqual(expected, actual)

    @mock.patch('fmn.formatters.fedmsg.meta.msg2long_form', mock.Mock(return_value='a'*500000))
    def test_email_too_big(self):
        """Assert huge single message emails are handled gracefully."""
        expected = (
            'Precedence: Bulk\n'
            'Auto-Submitted: auto-generated\n'
            'From: notifications@fedoraproject.org\n'
            'To: jeremy@jcline.org\n'
            'X-Fedmsg-Topic: org.fedoraproject.dev.fmn.filter.update\n'
            'X-Fedmsg-Category: fmn\n'
            'X-Fedmsg-Username: jcline\n'
            'X-Fedmsg-Num-Packages: 0\n'
            'Subject: jcline updated the rules on a fmn email filter\n'
            'MIME-Version: 1.0\n'
            'Content-Type: text/plain; charset="utf-8"\n'
            'Content-Transfer-Encoding: base64\n\n'
            'VGhpcyBtZXNzYWdlIHdhcyB0b28gbGFyZ2UgdG8gYmUgc2VudCEKVGhlIG1lc3NhZ2UgSUQgd2Fz\n'
            'OiAyMDE3LTZhYTcxZDViLWZiZTQtNDllNy1hZmRkLWFmY2YwZDIyODAyYgoK\n'
        )

        actual = formatters.email(self.message, self.recipient)
        self.assertEqual(expected, actual)

    @mock.patch.dict('fmn.formatters.config.app_conf', {'fmn.email.subject_prefix': 'PREFIX: '})
    def test_subject_prefix(self):
        """Assert the subject prefix is added if configured."""
        expected = (
            'Precedence: Bulk\n'
            'Auto-Submitted: auto-generated\n'
            'From: notifications@fedoraproject.org\n'
            'To: jeremy@jcline.org\n'
            'X-Fedmsg-Topic: org.fedoraproject.dev.fmn.filter.update\n'
            'X-Fedmsg-Category: fmn\n'
            'X-Fedmsg-Username: jcline\n'
            'X-Fedmsg-Num-Packages: 0\n'
            'Subject: PREFIX: jcline updated the rules on a fmn email filter\n'
            'MIME-Version: 1.0\n'
            'Content-Type: text/plain; charset="utf-8"\n'
            'Content-Transfer-Encoding: base64\n\n'
            'Tm90aWZpY2F0aW9uIHRpbWUgc3RhbXBlZCAyMDE3LTEwLTA2IDE3OjI1OjMwIFVUQwoKamNsaW5l\n'
            'IHVwZGF0ZWQgdGhlIHJ1bGVzIG9uIGEgZm1uIGVtYWlsIGZpbHRlcgoJaHR0cHM6Ly9hcHBzLmZl\n'
            'ZG9yYXByb2plY3Qub3JnL25vdGlmaWNhdGlvbnMv\n'
        )

        actual = formatters.email(self.message, self.recipient)
        self.assertEqual(expected, actual)

    def test_unparsable_category(self):
        """Assert failing to parse the topic works and just leaves those headers off."""
        expected = (
            'Precedence: Bulk\n'
            'Auto-Submitted: auto-generated\n'
            'From: notifications@fedoraproject.org\n'
            'To: jeremy@jcline.org\n'
            'X-Fedmsg-Topic: so.short\n'
            'X-Fedmsg-Num-Packages: 0\n'
            'Subject: fedmsg notification\n'
            'MIME-Version: 1.0\n'
            'Content-Type: text/plain; charset="utf-8"\n'
            'Content-Transfer-Encoding: base64\n\n'
            'Tm90aWZpY2F0aW9uIHRpbWUgc3RhbXBlZCAyMDE3LTEwLTA2IDE3OjI1OjMwIFVUQwoK\n'
        )
        self.message['topic'] = 'so.short'

        actual = formatters.email(self.message, self.recipient)
        self.assertEqual(expected, actual)

    @mock.patch('fmn.formatters.fedmsg.meta.msg2subtitle', mock.Mock(side_effect=Exception))
    def test_no_subtitle(self):
        """Assert an exception in msg2subtitle results in "fedmsg notification" as the subject."""
        expected = (
            'Precedence: Bulk\n'
            'Auto-Submitted: auto-generated\n'
            'From: notifications@fedoraproject.org\n'
            'To: jeremy@jcline.org\n'
            'X-Fedmsg-Topic: org.fedoraproject.dev.fmn.filter.update\n'
            'X-Fedmsg-Category: fmn\n'
            'X-Fedmsg-Username: jcline\n'
            'X-Fedmsg-Num-Packages: 0\n'
            'Subject: fedmsg notification\n'
            'MIME-Version: 1.0\n'
            'Content-Type: text/plain; charset="utf-8"\n'
            'Content-Transfer-Encoding: base64\n\n'
            'Tm90aWZpY2F0aW9uIHRpbWUgc3RhbXBlZCAyMDE3LTEwLTA2IDE3OjI1OjMwIFVUQwoKamNsaW5l\n'
            'IHVwZGF0ZWQgdGhlIHJ1bGVzIG9uIGEgZm1uIGVtYWlsIGZpbHRlcgoJaHR0cHM6Ly9hcHBzLmZl\n'
            'ZG9yYXByb2plY3Qub3JnL25vdGlmaWNhdGlvbnMv\n'
        )

        actual = formatters.email(self.message, self.recipient)
        self.assertEqual(expected, actual)

    @mock.patch('fmn.formatters.fedmsg.meta.msg2usernames', mock.Mock(side_effect=Exception))
    def test_unparsable_usernames(self):
        """Assert unparsable usernames just exclude that header."""
        expected = (
            'Precedence: Bulk\n'
            'Auto-Submitted: auto-generated\n'
            'From: notifications@fedoraproject.org\n'
            'To: jeremy@jcline.org\n'
            'X-Fedmsg-Topic: org.fedoraproject.dev.fmn.filter.update\n'
            'X-Fedmsg-Category: fmn\n'
            'X-Fedmsg-Num-Packages: 0\n'
            'Subject: jcline updated the rules on a fmn email filter\n'
            'MIME-Version: 1.0\n'
            'Content-Type: text/plain; charset="utf-8"\n'
            'Content-Transfer-Encoding: base64\n\n'
            'Tm90aWZpY2F0aW9uIHRpbWUgc3RhbXBlZCAyMDE3LTEwLTA2IDE3OjI1OjMwIFVUQwoKamNsaW5l\n'
            'IHVwZGF0ZWQgdGhlIHJ1bGVzIG9uIGEgZm1uIGVtYWlsIGZpbHRlcgoJaHR0cHM6Ly9hcHBzLmZl\n'
            'ZG9yYXByb2plY3Qub3JnL25vdGlmaWNhdGlvbnMv\n'
        )

        actual = formatters.email(self.message, self.recipient)
        self.assertEqual(expected, actual)

    @mock.patch('fmn.formatters.fedmsg.meta.msg2packages', mock.Mock(return_value=['pkg']))
    def test_packages(self):
        """Assert package headers are added."""
        expected = (
            'Precedence: Bulk\n'
            'Auto-Submitted: auto-generated\n'
            'From: notifications@fedoraproject.org\n'
            'To: jeremy@jcline.org\n'
            'X-Fedmsg-Topic: org.fedoraproject.dev.fmn.filter.update\n'
            'X-Fedmsg-Category: fmn\n'
            'X-Fedmsg-Username: jcline\n'
            'X-Fedmsg-Package: pkg\n'
            'X-Fedmsg-Num-Packages: 1\n'
            'Subject: jcline updated the rules on a fmn email filter\n'
            'MIME-Version: 1.0\n'
            'Content-Type: text/plain; charset="utf-8"\n'
            'Content-Transfer-Encoding: base64\n\n'
            'Tm90aWZpY2F0aW9uIHRpbWUgc3RhbXBlZCAyMDE3LTEwLTA2IDE3OjI1OjMwIFVUQwoKamNsaW5l\n'
            'IHVwZGF0ZWQgdGhlIHJ1bGVzIG9uIGEgZm1uIGVtYWlsIGZpbHRlcgoJaHR0cHM6Ly9hcHBzLmZl\n'
            'ZG9yYXByb2plY3Qub3JnL25vdGlmaWNhdGlvbnMv\n'
        )

        actual = formatters.email(self.message, self.recipient)
        self.assertEqual(expected, actual)

    @mock.patch('fmn.formatters.fedmsg.meta.msg2packages', mock.Mock(side_effect=Exception))
    def test_unparsable_packages(self):
        """Assert unparsable usernames just exclude that header."""
        expected = (
            'Precedence: Bulk\n'
            'Auto-Submitted: auto-generated\n'
            'From: notifications@fedoraproject.org\n'
            'To: jeremy@jcline.org\n'
            'X-Fedmsg-Topic: org.fedoraproject.dev.fmn.filter.update\n'
            'X-Fedmsg-Category: fmn\n'
            'X-Fedmsg-Username: jcline\n'
            'X-Fedmsg-Num-Packages: 0\n'
            'Subject: jcline updated the rules on a fmn email filter\n'
            'MIME-Version: 1.0\n'
            'Content-Type: text/plain; charset="utf-8"\n'
            'Content-Transfer-Encoding: base64\n\n'
            'Tm90aWZpY2F0aW9uIHRpbWUgc3RhbXBlZCAyMDE3LTEwLTA2IDE3OjI1OjMwIFVUQwoKamNsaW5l\n'
            'IHVwZGF0ZWQgdGhlIHJ1bGVzIG9uIGEgZm1uIGVtYWlsIGZpbHRlcgoJaHR0cHM6Ly9hcHBzLmZl\n'
            'ZG9yYXByb2plY3Qub3JnL25vdGlmaWNhdGlvbnMv\n'
        )

        actual = formatters.email(self.message, self.recipient)
        self.assertEqual(expected, actual)

    @mock.patch('fmn.formatters.fedmsg.meta.msg2long_form', mock.Mock(side_effect=Exception))
    def test_unparsable_body(self):
        """Assert the message JSON is sent if the long form fails."""
        expected = (
            'Precedence: Bulk\n'
            'Auto-Submitted: auto-generated\n'
            'From: notifications@fedoraproject.org\n'
            'To: jeremy@jcline.org\n'
            'X-Fedmsg-Topic: org.fedoraproject.dev.fmn.filter.update\n'
            'X-Fedmsg-Category: fmn\n'
            'X-Fedmsg-Username: jcline\n'
            'X-Fedmsg-Num-Packages: 0\n'
            'Subject: jcline updated the rules on a fmn email filter\n'
            'MIME-Version: 1.0\n'
            'Content-Type: text/plain; charset="utf-8"\n'
            'Content-Transfer-Encoding: base64\n\n'
            'Tm90aWZpY2F0aW9uIHRpbWUgc3RhbXBlZCAyMDE3LTEwLTA2IDE3OjI1OjMwIFVUQwoKewogICAg\n'
            'Im1zZyI6IHsKICAgICAgICAiY2hhbmdlZCI6ICJydWxlcyIsCiAgICAgICAgImNvbnRleHQiOiAi\n'
            'ZW1haWwiLAogICAgICAgICJvcGVuaWQiOiAiamNsaW5lLmlkLmZlZG9yYXByb2plY3Qub3JnIgog\n'
            'ICAgfSwKICAgICJtc2dfaWQiOiAiMjAxNy02YWE3MWQ1Yi1mYmU0LTQ5ZTctYWZkZC1hZmNmMGQy\n'
            'MjgwMmIiLAogICAgInRpbWVzdGFtcCI6IDE1MDczMTA3MzAsCiAgICAidG9waWMiOiAib3JnLmZl\n'
            'ZG9yYXByb2plY3QuZGV2LmZtbi5maWx0ZXIudXBkYXRlIiwKICAgICJ1c2VybmFtZSI6ICJ2YWdy\n'
            'YW50Igp9CglodHRwczovL2FwcHMuZmVkb3JhcHJvamVjdC5vcmcvbm90aWZpY2F0aW9ucy8=\n'
        )

        actual = formatters.email(self.message, self.recipient)
        self.assertEqual(expected, actual)

    @mock.patch('fmn.formatters.fedmsg.meta.msg2link', mock.Mock(side_effect=Exception))
    def test_unparsable_link(self):
        """Assert no link is included if none can be derived."""
        expected = (
            'Precedence: Bulk\n'
            'Auto-Submitted: auto-generated\n'
            'From: notifications@fedoraproject.org\n'
            'To: jeremy@jcline.org\n'
            'X-Fedmsg-Topic: org.fedoraproject.dev.fmn.filter.update\n'
            'X-Fedmsg-Category: fmn\n'
            'X-Fedmsg-Username: jcline\n'
            'X-Fedmsg-Num-Packages: 0\n'
            'Subject: jcline updated the rules on a fmn email filter\n'
            'MIME-Version: 1.0\n'
            'Content-Type: text/plain; charset="utf-8"\n'
            'Content-Transfer-Encoding: base64\n\n'
            'Tm90aWZpY2F0aW9uIHRpbWUgc3RhbXBlZCAyMDE3LTEwLTA2IDE3OjI1OjMwIFVUQwoKamNsaW5l\n'
            'IHVwZGF0ZWQgdGhlIHJ1bGVzIG9uIGEgZm1uIGVtYWlsIGZpbHRlcg==\n'
        )

        actual = formatters.email(self.message, self.recipient)
        self.assertEqual(expected, actual)

    def test_footer(self):
        """Assert no link is included if none can be derived."""
        expected = (
            'Precedence: Bulk\n'
            'Auto-Submitted: auto-generated\n'
            'From: notifications@fedoraproject.org\n'
            'To: jeremy@jcline.org\n'
            'X-Fedmsg-Topic: org.fedoraproject.dev.fmn.filter.update\n'
            'X-Fedmsg-Category: fmn\n'
            'X-Fedmsg-Username: jcline\n'
            'X-Fedmsg-Num-Packages: 0\n'
            'Subject: jcline updated the rules on a fmn email filter\n'
            'MIME-Version: 1.0\n'
            'Content-Type: text/plain; charset="utf-8"\n'
            'Content-Transfer-Encoding: base64\n\n'
            'Tm90aWZpY2F0aW9uIHRpbWUgc3RhbXBlZCAyMDE3LTEwLTA2IDE3OjI1OjMwIFVUQwoKamNsaW5l\n'
            'IHVwZGF0ZWQgdGhlIHJ1bGVzIG9uIGEgZm1uIGVtYWlsIGZpbHRlcgoJaHR0cHM6Ly9hcHBzLmZl\n'
            'ZG9yYXByb2plY3Qub3JnL25vdGlmaWNhdGlvbnMvCgotLQpZb3UgcmVjZWl2ZWQgdGhpcyBtZXNz\n'
            'YWdlIGR1ZSB0byB5b3VyIHByZWZlcmVuY2Ugc2V0dGluZ3MgYXQgCmh0dHA6Ly9sb2NhbGhvc3Q6\n'
            'NTAwMC9qY2xpbmUuaWQuZmVkb3JhcHJvamVjdC5vcmcvZW1haWwvMTE=\n'
        )
        self.recipient['triggered_by_links'] = True

        actual = formatters.email(self.message, self.recipient)
        self.assertEqual(expected, actual)


class EmailBatchTests(Base):

    def setUp(self):
        super(EmailBatchTests, self).setUp()
        self.messages = [
            {
                "msg": {
                    "changed": "rules",
                    "context": "email",
                    "openid": "jcline.id.fedoraproject.org"
                },
                "msg_id": "2017-6aa71d5b-fbe4-49e7-afdd-afcf0d22802b",
                "timestamp": 1507310730,
                "topic": "org.fedoraproject.dev.fmn.filter.update",
                "username": "vagrant",
            },
            {
                "msg": {
                    "changed": "rules",
                    "context": "email",
                    "openid": "bowlofeggs.id.fedoraproject.org"
                },
                "msg_id": "2017-6aa71d5b-aaaa-bbbb-cccc-afcf0d22802z",
                "timestamp": 1507310730,
                "topic": "org.fedoraproject.dev.fmn.filter.update",
                "username": "vagrant",
            },
        ]
        self.verbose_recipient = {
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
        self.not_verbose_recipient = {
            "email address": "jeremy@jcline.org",
            "filter_id": 11,
            "filter_name": "test",
            "filter_oneshot": False,
            "markup_messages": False,
            "shorten_links": False,
            "triggered_by_links": False,
            "user": "jcline.id.fedoraproject.org",
            "verbose": False,
        }

    def test_single_message(self):
        """Assert if the batch is of length one, it's the same as a plain email."""
        self.assertEqual(
            formatters.email(self.messages[0], self.verbose_recipient),
            formatters.email_batch([self.messages[0]], self.verbose_recipient),
        )

    def test_unique_username_headers(self):
        """Test that usernames are added only once for each in headers."""
        double_messages = self.messages * 2
        expected_start = (
            'Precedence: Bulk\n'
            'Auto-Submitted: auto-generated\n'
            'From: notifications@fedoraproject.org\n'
            'To: jeremy@jcline.org\n'
            'X-Fedmsg-Topic: org.fedoraproject.dev.fmn.filter.update\n'
            'X-Fedmsg-Category: fmn\n'
            'X-Fedmsg-Username: bowlofeggs\n'
            'X-Fedmsg-Username: jcline\n'
            'X-Fedmsg-Num-Packages: 0\n'
            'Subject: Fedora Notifications Digest (4 updates)\n'
            'MIME-Version: 1.0\n'
            'Content-Type: text/plain; charset="utf-8"\n'
            'Content-Transfer-Encoding: base64\n\n'
        )

        actual = formatters.email_batch(double_messages, self.verbose_recipient)
        self.assertIn(expected_start, actual)

    def test_basic_batch_verbose(self):
        """Assert a well-formed verbose email is returned from a basic message."""
        expected = (
            'Precedence: Bulk\n'
            'Auto-Submitted: auto-generated\n'
            'From: notifications@fedoraproject.org\n'
            'To: jeremy@jcline.org\n'
            'X-Fedmsg-Topic: org.fedoraproject.dev.fmn.filter.update\n'
            'X-Fedmsg-Category: fmn\n'
            'X-Fedmsg-Username: bowlofeggs\n'
            'X-Fedmsg-Username: jcline\n'
            'X-Fedmsg-Num-Packages: 0\n'
            'Subject: Fedora Notifications Digest (2 updates)\n'
            'MIME-Version: 1.0\n'
            'Content-Type: text/plain; charset="utf-8"\n'
            'Content-Transfer-Encoding: base64\n\n'
            'RGlnZXN0IFN1bW1hcnk6CjEuCWpjbGluZSB1cGRhdGVkIHRoZSBydWxlcyBvbiBhIGZtbiBlbWFp\n'
            'bCBmaWx0ZXIKMi4JYm93bG9mZWdncyB1cGRhdGVkIHRoZSBydWxlcyBvbiBhIGZtbiBlbWFpbCBm\n'
            'aWx0ZXIKCi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t\n'
            'LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KCigyMDE3LTEwLTA2IDE3OjI1OjMwIFVUQykg\n'
            'amNsaW5lIHVwZGF0ZWQgdGhlIHJ1bGVzIG9uIGEgZm1uIGVtYWlsIGZpbHRlcgotIGh0dHBzOi8v\n'
            'YXBwcy5mZWRvcmFwcm9qZWN0Lm9yZy9ub3RpZmljYXRpb25zLwoKamNsaW5lIHVwZGF0ZWQgdGhl\n'
            'IHJ1bGVzIG9uIGEgZm1uIGVtYWlsIGZpbHRlcgoKLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t\n'
            'LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQoKKDIw\n'
            'MTctMTAtMDYgMTc6MjU6MzAgVVRDKSBib3dsb2ZlZ2dzIHVwZGF0ZWQgdGhlIHJ1bGVzIG9uIGEg\n'
            'Zm1uIGVtYWlsIGZpbHRlcgotIGh0dHBzOi8vYXBwcy5mZWRvcmFwcm9qZWN0Lm9yZy9ub3RpZmlj\n'
            'YXRpb25zLwoKYm93bG9mZWdncyB1cGRhdGVkIHRoZSBydWxlcyBvbiBhIGZtbiBlbWFpbCBmaWx0\n'
            'ZXI=\n'
        )

        actual = formatters.email_batch(self.messages, self.verbose_recipient)
        self.assertEqual(expected, actual)

    def test_basic_batch_not_verbose(self):
        """Assert a well-formed not verbose email is returned from a basic message."""
        expected = (
            'Precedence: Bulk\n'
            'Auto-Submitted: auto-generated\n'
            'From: notifications@fedoraproject.org\n'
            'To: jeremy@jcline.org\n'
            'X-Fedmsg-Topic: org.fedoraproject.dev.fmn.filter.update\n'
            'X-Fedmsg-Category: fmn\n'
            'X-Fedmsg-Username: bowlofeggs\n'
            'X-Fedmsg-Username: jcline\n'
            'X-Fedmsg-Num-Packages: 0\n'
            'Subject: Fedora Notifications Digest (2 updates)\n'
            'MIME-Version: 1.0\n'
            'Content-Type: text/plain; charset="utf-8"\n'
            'Content-Transfer-Encoding: base64\n\n'
            'KDIwMTctMTAtMDYgMTc6MjU6MzAgVVRDKSBqY2xpbmUgdXBkYXRlZCB0aGUgcnVsZXMgb24gYSBm\n'
            'bW4gZW1haWwgZmlsdGVyCi0gaHR0cHM6Ly9hcHBzLmZlZG9yYXByb2plY3Qub3JnL25vdGlmaWNh\n'
            'dGlvbnMvCgotLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t\n'
            'LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCgooMjAxNy0xMC0wNiAxNzoyNTozMCBVVEMp\n'
            'IGJvd2xvZmVnZ3MgdXBkYXRlZCB0aGUgcnVsZXMgb24gYSBmbW4gZW1haWwgZmlsdGVyCi0gaHR0\n'
            'cHM6Ly9hcHBzLmZlZG9yYXByb2plY3Qub3JnL25vdGlmaWNhdGlvbnMv\n'
        )

        actual = formatters.email_batch(self.messages, self.not_verbose_recipient)
        self.assertEqual(expected, actual)

    def test_too_many_messages(self):
        """Test batch content when too many messages are queued."""
        big_batch = self.messages * 500
        expected = (
            'Precedence: Bulk\n'
            'Auto-Submitted: auto-generated\n'
            'From: notifications@fedoraproject.org\n'
            'To: jeremy@jcline.org\n'
            'Subject: Fedora Notifications Digest error\n'
            'MIME-Version: 1.0\n'
            'Content-Type: text/plain; charset="utf-8"\n'
            'Content-Transfer-Encoding: base64\n\n'
            'VG9vIG1hbnkgbWVzc2FnZXMgd2VyZSBxdWV1ZWQgdG8gYmUgc2VudCBpbiB0aGlzIGRpZ2VzdCAo\n'
            'MTAwMCkhCkNvbnNpZGVyIGFkanVzdGluZyB5b3VyIEZNTiBzZXR0aW5ncy4K\n'
        )

        actual = formatters.email_batch(big_batch, self.verbose_recipient)
        self.assertEqual(expected, actual)

    @mock.patch('fmn.formatters.fedmsg.meta.msg2long_form', mock.Mock(return_value=u'a' * 250000))
    def test_digest_content_too_long(self):
        """Test batch content when it exceeds 500k characters limit."""
        expected = (
            'Precedence: Bulk\n'
            'Auto-Submitted: auto-generated\n'
            'From: notifications@fedoraproject.org\n'
            'To: jeremy@jcline.org\n'
            'X-Fedmsg-Topic: org.fedoraproject.dev.fmn.filter.update\n'
            'X-Fedmsg-Category: fmn\n'
            'X-Fedmsg-Username: bowlofeggs\n'
            'X-Fedmsg-Username: jcline\n'
            'X-Fedmsg-Num-Packages: 0\n'
            'Subject: Fedora Notifications Digest (2 updates)\n'
            'MIME-Version: 1.0\n'
            'Content-Type: text/plain; charset="utf-8"\n'
            'Content-Transfer-Encoding: base64\n\n'
            'VGhpcyBtZXNzYWdlIGRpZ2VzdCB3YXMgdG9vIGxhcmdlIHRvIGJlIHNlbnQhClRoZSBmb2xsb3dp\n'
            'bmcgbWVzc2FnZXMgd2VyZSBiYXRjaGVkOgoKMjAxNy02YWE3MWQ1Yi1mYmU0LTQ5ZTctYWZkZC1h\n'
            'ZmNmMGQyMjgwMmIKMjAxNy02YWE3MWQ1Yi1hYWFhLWJiYmItY2NjYy1hZmNmMGQyMjgwMnoK\n'
        )

        actual = formatters.email_batch(self.messages, self.verbose_recipient)
        self.assertEqual(expected, actual)
