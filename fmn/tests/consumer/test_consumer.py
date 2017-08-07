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
"""Tests for the :mod:`fmn.consumer.consumer` module"""
from __future__ import absolute_import

import unittest

import mock

from fmn.consumer import consumer


class FMNConsumerTests(unittest.TestCase):

    def setUp(self):
        self.config = {
            'fmn.consumer.enabled': True,
            'validate_signatures': False,
            'fmn.sqlalchemy.uri': 'sqlite://',
        }
        self.hub = mock.Mock(config=self.config)

    def test_default_topic(self):
        """Assert the default topic for the FMN consumer is everything."""
        fmn_consumer = consumer.FMNConsumer(self.hub)

        self.assertEqual(b'*', fmn_consumer.topic)
        self.hub.subscribe.assert_called_once_with(b'*', fmn_consumer._consume_json)

    def test_custom_topics(self):
        """Assert the default topic for the FMN consumer is everything."""
        self.config['fmn.topics'] = [b'my.custom.topic']
        fmn_consumer = consumer.FMNConsumer(self.hub)

        self.assertEqual([b'my.custom.topic'], fmn_consumer.topic)
        self.hub.subscribe.assert_called_once_with(b'my.custom.topic', fmn_consumer._consume_json)
