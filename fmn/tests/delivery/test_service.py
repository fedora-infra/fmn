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
from __future__ import absolute_import

import unittest

from kombu import Queue, Consumer
from mock import Mock, patch

from fmn.delivery import service
from fmn.lib import models
from fmn.tests import Base


class ConsumerTests(unittest.TestCase):
    """Tests for the :class:`fmn.delivery.service.Consumer` class."""

    def test_get_consumers(self):
        """Assert the ``get_consumers`` interface provides a consumer with a callback."""
        consumer = service.Consumer(None, 'backends')

        consumers = consumer.get_consumers(Consumer, Mock())

        self.assertEqual(1, len(consumers))
        self.assertEqual([consumer.on_message], consumers[0].callbacks)

    def test_single_queue(self):
        """Assert a single queue as a string is supported."""
        consumer = service.Consumer(None, 'backends')

        self.assertEqual([Queue('backends')], consumer.queues)

    def test_multiple_queues(self):
        """Assert multiple queues are created when provided."""
        queues = ['backends.email', 'backends.irc']

        consumer = service.Consumer(None, queues)

        self.assertEqual([Queue(q) for q in queues], consumer.queues)

    def test_stop(self):
        """Assert calling stop sets the ``should_stop`` flag."""
        consumer = service.Consumer(None, 'backends')
        self.assertFalse(consumer.should_stop)

        consumer.stop()
        self.assertTrue(consumer.should_stop)

    @patch('fmn.delivery.service.threads.blockingCallFromThread')
    def test_on_message(self, mock_blocking):
        """Assert messages are passed on to the Twisted DeliveryService."""
        message = Mock()
        mock_delivery = Mock()
        consumer = service.Consumer(mock_delivery, 'backends')

        consumer.on_message({'hello': 'world'}, message)

        mock_blocking.assert_called_with(
            service.reactor, mock_delivery.handle_message, {'hello': 'world'})
        message.ack.assert_called_once_with()

    @patch('fmn.delivery.service.connections')
    @patch('fmn.delivery.service.threads.blockingCallFromThread')
    def test_on_message_failed_delivery(self, mock_blocking_call, mock_conns):
        """Assert general exceptions in the delivery service re-queue the message."""
        mock_blocking_call.side_effect = Exception
        message = Mock()
        consumer = service.Consumer(Mock(), 'backends')
        conn = mock_conns.__getitem__.return_value.acquire.return_value.__enter__.return_value

        consumer.on_message({'hello': 'world'}, message)

        conn.Producer.return_value.publish.assert_called_with(
            {'hello': 'world'}, routing_key='backends')
        message.ack.assert_called_once_with()


class DeliveryServiceTests(Base):
    """Tests for the :class:`fmn.delivery.service.DeliveryService` class."""

    @patch('fmn.delivery.service.task')
    @patch('fmn.delivery.service.reactor')
    def test_start_service(self, mock_reactor, mock_task):
        """Assert startService creates a looping call for confirmations and starts the consumer."""
        test_config = {
            'fmn.backends.debug': True,
        }
        delivery_service = service.DeliveryService()

        with patch.dict(service.config.app_conf, test_config):
            delivery_service.startService()

        mock_reactor.callInThread.assert_called_with(delivery_service.consumer.run)
        mock_task.LoopingCall.assert_called_with(delivery_service.handle_confirmations)
        delivery_service.confirmation_loop.start.assert_called_with(10)

    @patch('fmn.delivery.service.task')
    @patch('fmn.delivery.service.reactor')
    def test_confirmation_frequency(self, mock_reactor, mock_task):
        """Assert the confirmation loop frequency is configurable."""
        test_config = {
            'fmn.backends.debug': True,
            'fmn.confirmation_frequency': 15,
        }
        delivery_service = service.DeliveryService()

        with patch.dict(service.config.app_conf, test_config):
            delivery_service.startService()

        delivery_service.confirmation_loop.start.assert_called_with(15)

    @patch('fmn.delivery.service.task')
    @patch('fmn.delivery.service.reactor')
    def test_prune_backends(self, mock_reactor, mock_task):
        """Assert backends are pruned to match the configured backends."""
        test_config = {
            'fmn.backends.debug': True,
            'fmn.confirmation_frequency': 15,
            'fmn.backends': ['sse'],
        }
        delivery_service = service.DeliveryService()

        with patch.dict(service.config.app_conf, test_config):
            delivery_service.startService()

        self.assertEqual(1, len(delivery_service.backends))
        self.assertTrue('sse' in delivery_service.backends)

    @patch('fmn.delivery.service.task')
    @patch('fmn.delivery.service.reactor')
    def test_invalid_backends(self, mock_reactor, mock_task):
        """Assert an invalid backend in the configuration raises a ValueError."""
        test_config = {
            'fmn.backends.debug': True,
            'fmn.confirmation_frequency': 15,
            'fmn.backends': ['carrier bird'],
        }
        delivery_service = service.DeliveryService()

        with patch.dict(service.config.app_conf, test_config):
            self.assertRaises(ValueError, delivery_service.startService)

    @patch('fmn.delivery.service._log')
    def test_handle_message_missing_key(self, mock_log):
        """Assert a message missing a key is logged."""
        delivery_service = service.DeliveryService()

        delivery_service.handle_message(None)

        mock_log.exception.assert_called_with('Received a malformed message, "%r", from the'
                                              ' backend queue, dropping message!', None)

    @patch('fmn.delivery.service.task', Mock())
    @patch('fmn.delivery.service.reactor', Mock())
    @patch('fmn.delivery.service._log')
    def test_handle_message_missing_backend(self, mock_log):
        """Assert when the backend doesn't exist for the message, an error is logged."""
        delivery_service = service.DeliveryService()
        message = {
            'context': 'carrier bird',
            'recipient': {},
            'fedmsg': {},
            'formatted_message': ''
        }
        test_config = {
            'fmn.backends.debug': True,
            'fmn.confirmation_frequency': 15,
            'fmn.backends': ['sse'],
        }
        delivery_service = service.DeliveryService()
        with patch.dict(service.config.app_conf, test_config):
            delivery_service.startService()

        delivery_service.handle_message(message)

        mock_log.error.assert_called_with(
            'Delivery request to the "%s" backend failed because there is no '
            'backend loaded with that name', 'carrier bird')

    @patch('fmn.delivery.service.task', Mock())
    @patch('fmn.delivery.service.reactor', Mock())
    @patch('fmn.delivery.service._log')
    def test_handle_message(self, mock_log):
        """Assert well-formed messages are handled."""
        delivery_service = service.DeliveryService()
        message = {
            'context': 'sse',
            'recipient': {},
            'fedmsg': {},
            'formatted_message': ''
        }
        test_config = {
            'fmn.backends.debug': True,
            'fmn.confirmation_frequency': 15,
            'fmn.backends': ['sse'],
        }
        delivery_service = service.DeliveryService()
        with patch.dict(service.config.app_conf, test_config):
            delivery_service.startService()

        delivery_service.handle_message(message)

        mock_log.info.assert_called_with(
            'Successfully delivered message %s to %s via %s', 'UNKNOWN_ID', 'UNKOWN_USER', 'sse')

    @patch('fmn.delivery.service._log')
    def test_handle_message_error(self, mock_log):
        """Assert a general exception while handling a message is logged."""
        delivery_service = service.DeliveryService()
        message = {
            'context': 'sse',
            'recipient': {},
            'fedmsg': {},
            'formatted_message': ''
        }
        delivery_service = service.DeliveryService()
        mock_backend = Mock()
        mock_backend.deliver.side_effect = Exception
        delivery_service.backends = {'sse': mock_backend}

        delivery_service.handle_message(message)

        mock_log.exception.assert_called_with(
            'The "%s" backend raised an unexpected exception while trying to '
            'deliver a notification to recipient "%r"', 'sse', {})

    @patch('fmn.delivery.service.reactor', Mock())
    @patch('fmn.delivery.service.task', Mock())
    def test_stop_service(self):
        """Assert stopService forwards to the looping confirmation call and the consumer."""
        test_config = {
            'fmn.backends.debug': True,
            'fmn.confirmation_frequency': 15,
            'fmn.backends': ['sse'],
        }
        delivery_service = service.DeliveryService()
        with patch.dict(service.config.app_conf, test_config):
            delivery_service.startService()

        self.assertFalse(delivery_service.consumer.should_stop)
        delivery_service.stopService()

        self.assertTrue(delivery_service.consumer.should_stop)
        delivery_service.confirmation_loop.stop.assert_called_with()

    def test_handle_confirmations(self):
        """Assert confirmations are handled with the backend"""
        user = models.User(
            openid='jcline.id.fedoraproject.org', openid_url='http://jcline.id.fedoraproject.org')
        context = models.Context(
            name='sse', description='description', detail_name='SSE', icon='wat')
        confirmation = models.Confirmation(detail_value='eh', user=user, context=context)
        self.sess.add(confirmation)
        self.sess.commit()
        delivery_service = service.DeliveryService()
        mock_backend = Mock()
        delivery_service.backends = {'sse': mock_backend}

        delivery_service.handle_confirmations()

        mock_backend.handle_confirmation.assert_called_once_with(models.Session(), confirmation)

    @patch('fmn.delivery.service._log')
    def test_handle_confirmation_failed(self, mock_log):
        """Assert exceptions are reported, but aren't raised."""
        user = models.User(
            openid='jcline.id.fedoraproject.org', openid_url='http://jcline.id.fedoraproject.org')
        context = models.Context(
            name='sse', description='description', detail_name='SSE', icon='wat')
        confirmation = models.Confirmation(detail_value='eh', user=user, context=context)
        self.sess.add(confirmation)
        self.sess.commit()
        delivery_service = service.DeliveryService()
        mock_backend = Mock()
        mock_backend.handle_confirmation.side_effect = Exception
        delivery_service.backends = {'sse': mock_backend}

        delivery_service.handle_confirmations()

        mock_log.exception.assert_called_with(
            'Unexpected exception while trying to handle a confirmation')
