# -*- coding: utf-8 -*-
#
# This file is part of FMN.
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
"""Tests for the :mod:`fmn.consumer.backends.mail` module"""
from __future__ import absolute_import, unicode_literals

import unittest

from fmn.consumer.backends import mail


class InitTests(unittest.TestCase):
    """Test email backend initialization"""


class CreateMessageTests(unittest.TestCase):
    """Tests for the create_message function"""

    def setUp(self):
        self.config = {
            'fmn.email.mailserver': 'smtp.example.com',
            'fmn.email.from_address': 'nobody@example.com',
        }
        self.backend = mail.EmailBackend(self.config)
        self.recipient = {
            'email address': 'user@example.com',
            'triggered_by_links': False,
        }

    def test_create_message_to_header(self):
        """Assert messages have the To header set"""
        message = self.backend._create_message(self.recipient, 'Test subject', 'my content')

        self.assertTrue('To' in message)
        self.assertEqual('user@example.com', message['To'])

    def test_create_message_from_header(self):
        """Assert messages have the From header set"""
        message = self.backend._create_message(self.recipient, 'Test subject', 'my content')

        self.assertTrue('From' in message)
        self.assertEqual('nobody@example.com', message['From'])

    def test_create_message_subject_header(self):
        """Assert messages have the Subject header set"""
        message = self.backend._create_message(self.recipient, 'Test subject', 'my content')

        self.assertTrue('Subject' in message)
        self.assertEqual('Test subject', message['Subject'])

    def test_create_message_autosubmit_header(self):
        """Assert messages have the Auto-Submitted header set"""
        message = self.backend._create_message(self.recipient, 'Test subject', 'my content')
        self.assertEqual('auto-generated', message['Auto-Submitted'])

    def test_create_message_precedence_header(self):
        """Assert messages have the Precedence header set"""
        message = self.backend._create_message(self.recipient, 'Test subject', 'my content')
        self.assertEqual('Bulk', message['Precendence'])

    def test_create_message_no_topic_header(self):
        """Assert messages without topics have no X-Fedmsg-Topic header set"""
        message = self.backend._create_message(self.recipient, 'Test subject', 'my content')
        self.assertEqual(None, message['X-Fedmsg-Topic'])

    def test_create_message_topic_header(self):
        """Assert messages with topics have X-Fedmsg-Topic headers set"""
        message = self.backend._create_message(
            self.recipient, 'Test subject', 'my content', topics=['topic1', 'topic2'])
        self.assertEqual(sorted(['topic1', 'topic2']), sorted(message.get_all('X-Fedmsg-Topic')))

    def test_create_message_no_category_header(self):
        """Assert messages without categories have no X-Fedmsg-Category header set"""
        message = self.backend._create_message(self.recipient, 'Test subject', 'my content')
        self.assertEqual(None, message['X-Fedmsg-Category'])

    def test_create_message_category_header(self):
        """Assert messages with categories have X-Fedmsg-Category headers set"""
        message = self.backend._create_message(
            self.recipient, 'Test subject', 'my content', categories=['cat1', 'cat2'])
        self.assertEqual(sorted(['cat1', 'cat2']), sorted(message.get_all('X-Fedmsg-Category')))

    def test_create_message_no_username_header(self):
        """Assert messages without usernames have no X-Fedmsg-Username header set"""
        message = self.backend._create_message(self.recipient, 'Test subject', 'my content')
        self.assertEqual(None, message['X-Fedmsg-Username'])

    def test_create_message_username_header(self):
        """Assert messages with usernames have X-Fedmsg-Username header set"""
        message = self.backend._create_message(
            self.recipient, 'Test subject', 'my content', usernames=['jcline', 'bowlofeggs'])
        self.assertEqual(
            sorted(['jcline', 'bowlofeggs']), sorted(message.get_all('X-Fedmsg-Username')))

    def test_create_message_no_package_header(self):
        """Assert messages without packages have no X-Fedmsg-Package header set"""
        message = self.backend._create_message(self.recipient, 'Test subject', 'my content')
        self.assertEqual(None, message['X-Fedmsg-Package'])

    def test_create_message_package_header(self):
        """Assert messages with packages have X-Fedmsg-Package header set"""
        message = self.backend._create_message(
            self.recipient, 'Test subject', 'my content', packages=['glibc', 'kernel'])
        self.assertEqual(
            sorted(['glibc', 'kernel']), sorted(message.get_all('X-Fedmsg-Package')))

    def test_basic_create_message(self):
        """Assert a basic message rendered as a string is sane"""
        expected_message = """To: user@example.com
From: nobody@example.com
Precendence: Bulk
Auto-Submitted: auto-generated
Subject: Test subject
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: base64

bXkgY29udGVudA==
""".encode('utf-8')
        message = self.backend._create_message(self.recipient, 'Test subject', 'my content')
        self.assertEqual(expected_message, message.as_string())

    def test_create_message(self):
        """Assert a message with all possible headers rendered as a string is sane"""
        expected_message = """To: user@example.com
From: nobody@example.com
Precendence: Bulk
Auto-Submitted: auto-generated
X-Fedmsg-Topic: topic1
X-Fedmsg-Category: cat1
X-Fedmsg-Username: jcline
X-Fedmsg-Package: python-requests
Subject: Test subject
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: base64

bXkgY29udGVudA==
""".encode('utf-8')
        message = self.backend._create_message(
            self.recipient,
            'Test subject',
            'my content',
            topics=['topic1'],
            categories=['cat1'],
            usernames=['jcline'],
            packages=['python-requests']
        )
        self.assertEqual(expected_message, message.as_string())
