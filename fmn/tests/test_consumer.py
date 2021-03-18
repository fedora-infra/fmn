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

import mock

from fmn import consumer, config
from fmn.tests import Base


class FMNConsumerTests(Base):

    def setUp(self):
        super(FMNConsumerTests, self).setUp()
        self.config = config._FmnConfig()
        self.config['fmn.sqlalchemy.uri'] = 'sqlite://'
        self.config['fmn.consumer.enabled'] = True
        self.config['validate_signatures'] = False
        self.hub = mock.Mock(config=self.config)

    @mock.patch('fmn.consumer.heat_fas_cache', mock.Mock())
    def test_default_topic(self):
        """Assert the default topic for the FMN consumer is everything."""
        fmn_consumer = consumer.FMNConsumer(self.hub)

        self.assertEqual([b'*'], fmn_consumer.topic)
        self.hub.subscribe.assert_called_once_with(b'*', fmn_consumer._consume_json)

    @mock.patch('fmn.consumer.heat_fas_cache', mock.Mock())
    def test_custom_topics(self):
        """Assert the default topic for the FMN consumer is everything."""
        self.config['fmn.topics'] = [b'my.custom.topic']
        with mock.patch.dict(consumer.config.app_conf, self.config):
            fmn_consumer = consumer.FMNConsumer(self.hub)

        self.assertEqual([b'my.custom.topic'], fmn_consumer.topic)
        self.hub.subscribe.assert_called_once_with(b'my.custom.topic', fmn_consumer._consume_json)

    @mock.patch('fmn.consumer.heat_fas_cache')
    def test_heat_cache(self, mock_heat):
        """Assert a task is dispatched to heat the cache on startup."""
        consumer.FMNConsumer(self.hub)

        mock_heat.apply_async.assert_called_once_with()

    @mock.patch('fmn.consumer.heat_fas_cache', mock.Mock())
    @mock.patch('fmn.consumer.find_recipients')
    def test_refresh_cache_fmn_message(self, mock_find_recipients):
        """Assert messages with an '.fmn.' topic result in a message to workers."""
        fmn_consumer = consumer.FMNConsumer(self.hub)
        fmn_consumer.autocreate = False
        message = {
            'topic': 'com.example.fmn.topic',
            'body': {
                'msg_id': '12',
                'msg': {'openid': 'jcline.id.fedoraproject.org'},
                'topic': 'com.example.topic',
            }
        }
        fmn_consumer.work(self.sess, message)

        self.assertEqual(
            mock_find_recipients.apply_async.call_args_list[0][0][0],
            ({'topic': 'fmn.internal.refresh_cache', 'body': 'jcline.id.fedoraproject.org'},),
        )
        self.assertEqual(
            mock_find_recipients.apply_async.call_args_list[0][1],
            dict(exchange='fmn.tasks.reload_cache',
                 routing_key=self.config['celery']['task_default_queue']),
        )

    @mock.patch('fmn.consumer.heat_fas_cache', mock.Mock())
    @mock.patch('fmn.consumer.new_packager', mock.Mock(return_value='jcline'))
    @mock.patch('fmn.consumer.get_fas_email', mock.Mock(return_value='jcline'))
    @mock.patch('fmn.consumer.find_recipients')
    def test_refresh_cache_auto_create(self, mock_find_recipients):
        """Assert messages with an '.fmn.' topic result in a message to workers."""
        fmn_consumer = consumer.FMNConsumer(self.hub)
        fmn_consumer.autocreate = True
        message = {
            'topic': 'com.example.topic',
            'body': {
                'msg_id': '12',
                'topic': 'com.example.topic',
            }
        }
        fmn_consumer.work(self.sess, message)

        self.assertEqual(
            mock_find_recipients.apply_async.call_args_list[0][0][0],
            ({'topic': 'fmn.internal.refresh_cache', 'body': 'jcline.id.fedoraproject.org'},),
        )
        self.assertEqual(
            mock_find_recipients.apply_async.call_args_list[0][1],
            dict(exchange='fmn.tasks.reload_cache'),
        )
