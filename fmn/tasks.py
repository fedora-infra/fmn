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
This module contains the `Celery tasks`_ used by FMN.

.. _Celery tasks: http://docs.celeryproject.org/en/latest/
"""

from __future__ import absolute_import

import datetime

from celery.utils.log import get_task_logger
from fedmsg_meta_fedora_infrastructure import fasshim
from kombu import Connection, Queue
from kombu.pools import connections
from celery import task
import fedmsg
import fedmsg.meta
import fedmsg_meta_fedora_infrastructure

from . import config, lib as fmn_lib, formatters, exceptions
from . import fmn_fasshim
from .lib import models
from .celery import app
from .constants import BACKEND_QUEUE_PREFIX


__all__ = ['find_recipients']


_log = get_task_logger(__name__)


REFRESH_CACHE_TOPIC = 'fmn.internal.refresh_cache'


# Monkey patch fedmsg_meta modules
fasshim.nick2fas = fmn_fasshim.nick2fas
fasshim.email2fas = fmn_fasshim.email2fas
fedmsg_meta_fedora_infrastructure.supybot.nick2fas = fmn_fasshim.nick2fas
fedmsg_meta_fedora_infrastructure.anitya.email2fas = fmn_fasshim.email2fas
fedmsg_meta_fedora_infrastructure.bz.email2fas = fmn_fasshim.email2fas
fedmsg_meta_fedora_infrastructure.mailman3.email2fas = fmn_fasshim.email2fas
fedmsg_meta_fedora_infrastructure.pagure.email2fas = fmn_fasshim.email2fas


class _FindRecipients(task.Task):
    """A Celery task sub-class that loads and caches user preferences."""

    name = 'fmn.tasks.find_recipients'
    # Retry tasks every hour for 60 days before giving up
    default_retry_delay = 3600
    max_retries = 1440
    autoretry_for = (Exception,)

    def __init__(self):
        """
        Initialize caches and other resources for the tasks that require user preferences.

        This is run once per process, not per task.
        """
        _log.info('Initializing the "%s" task', self.name)
        fedmsg.meta.make_processors(**config.app_conf)
        self._valid_paths = None
        self._user_preferences = None
        _log.info('Initialization complete for the "%s" task', self.name)

    @property
    def valid_paths(self):
        """
        A property that lazy-loads the valid paths for FMN rules.

        This is done here rather in ``__init__`` so that users of this task
        don't load all the valid paths when the task is registered with
        Celery.
        """
        if self._valid_paths is None:
            _log.info('Loading valid FMN rule paths')
            self._valid_paths = fmn_lib.load_rules(root="fmn.rules")
            _log.info('All FMN rule paths successfully loaded')
        return self._valid_paths

    @property
    def user_preferences(self):
        """
        A property that lazy-loads the user preferences.

        This is done here rather in ``__init__`` so that users of this task
        don't load all the user preferences when the task is registered with
        Celery.
        """
        if self._user_preferences is None:
            _log.info('Loading all user preferences from the database')
            self._user_preferences = fmn_lib.load_preferences(
                cull_disabled=True, cull_backends=['desktop'])
            _log.info('All user preferences successfully loaded from the database')
        return self._user_preferences

    def run(self, message):
        """
        A Celery task that finds a list of recipients for a message.

        When the recipients have been found, it publishes an AMQP message for each
        context (backend) in the format::

            {
                'context': <backend>,
                'recipients': [
                    {
                      "triggered_by_links": true,
                      "markup_messages": false,
                      "user": "jcline.id.fedoraproject.org",
                      "filter_name": "firehose",
                      "filter_oneshot": false,
                      "filter_id": 7,
                      "shorten_links": false,
                      "verbose": true,
                    },
                ]
                'raw_msg': the message that this task handled,
            }


        Args:
            self (celery.Task): The instance of the Task object this function is bound to.
            message (dict): A fedmsg to find recipients for.
        """
        _log.debug('Determining recipients for message "%r"', message)
        topic, message_body = message['topic'], message['body']

        # We send a fake message with this topic as a broadcast to all workers in order for them
        # to refresh their caches, so if this message is a cache refresh notification stop early.
        if topic == REFRESH_CACHE_TOPIC:
            _log.info('Refreshing the user preferences for %s', message_body)
            fmn_lib.update_preferences(message_body, self.user_preferences)
            return

        results = fmn_lib.recipients(
             self.user_preferences, message_body, self.valid_paths, config.app_conf)
        _log.info('Found %s recipients for message %s', sum(map(len, results.values())),
                  message_body.get('msg_id', topic))

        self._queue_for_delivery(results, message)

    def _queue_for_delivery(self, results, message):
        """
        Queue a processed message for delivery to its recipients.

        The message is either delivered to the default AMQP exchange with the 'backends'
        routing key or placed in the database if the user has enabled batch delivery. If
        it is placed in the database, the :func:`batch_messages` task will handle its
        delivery.

        Message format::
            {
              "context": "email",
              "recipient": dict,
              "fedmsg": dict,
              "formatted_message": <formatted_message>
            }

        Args:
            results (dict): A dictionary where the keys are context names and the values are
                a list of recipients for that context. A recipient entry in the list is a
                dictionary. See :func:`fmn.lib.recipients` for the dictionary format.
            message (dict): The raw fedmsg to humanize and deliver to the given recipients.
        """
        session = models.Session()
        broker_url = config.app_conf['celery']['broker']

        with connections[Connection(broker_url)].acquire(block=True, timeout=60) as conn:
            producer = conn.Producer()
            for context, recipients in results.items():
                _log.info('Dispatching messages for %d recipients for the %s backend',
                          len(recipients), context)
                for recipient in recipients:
                    user = recipient['user']
                    preference = self.user_preferences['{}_{}'.format(user, context)]

                    if ('filter_oneshot' in recipient and recipient['filter_oneshot']):
                        _log.info('Marking one-time filter as fired')
                        idx = recipient['filter_id']
                        fltr = models.Filter.query.get(idx)
                        fltr.fired(session)

                    if preference.get('batch_delta') or preference.get('batch_count'):
                        _log.info('User "%s" has batch delivery set; placing message in database',
                                  user)
                        models.QueuedMessage.enqueue(session, user, context, message)
                        continue

                    formatted_message = None
                    if context == 'email':
                        formatted_message = formatters.email(message['body'], recipient)
                    elif context == 'irc':
                        formatted_message = formatters.irc(message['body'], recipient)
                    elif context == 'sse':
                        try:
                            formatted_message = formatters.sse(message['body'], recipient)
                        except Exception:
                            _log.exception('An exception occurred formatting the message '
                                           'for delivery: falling back to sending the raw fedmsg')
                            formatted_message = message

                    if formatted_message is None:
                        raise exceptions.FmnError(
                            'The message was not formatted in any way, aborting!')

                    _log.info('Queuing message for delivery to %s on the %s backend', user, context)
                    backend_message = {
                        "context": context,
                        "recipient": recipient,
                        "fedmsg": message,
                        "formatted_message": formatted_message,
                    }
                    routing_key = BACKEND_QUEUE_PREFIX + context
                    producer.publish(backend_message, routing_key=routing_key,
                                     declare=[Queue(routing_key, durable=True)])
                    session.commit()


@app.task(name='fmn.tasks.batch_messages', ignore_results=True)
def batch_messages():
    """
    A task that collects all messages ready for batch delivery and queues them.

    Messages for users of the batch feature are placed in the database by the
    :func:`find_recipients` task. Those messages are then picked up by this task,
    turned into a summary using the :mod:`fmn.formatters` module, and placed in
    the delivery service's AMQP queue.

    This is intended to be run as a periodic task using Celery's beat service.
    """
    session = models.Session()
    broker_url = config.app_conf['celery']['broker']
    with connections[Connection(broker_url)].acquire(block=True, timeout=60) as conn:
        producer = conn.Producer()
        for pref in models.Preference.list_batching(session):
            if not _batch_ready(pref):
                continue

            queued_messages = models.QueuedMessage.list_for(
                session, pref.user, pref.context)
            _log.info('Batching %d queued messages for %s', len(queued_messages), pref.user.openid)

            messages = [m.message for m in queued_messages]
            recipients = [
                {
                    pref.context.detail_name: value.value,
                    'user': pref.user.openid,
                    'markup_messages': pref.markup_messages,
                    'triggered_by_links': pref.triggered_by_links,
                    'shorten_links': pref.shorten_links,
                }
                for value in pref.detail_values
            ]
            for recipient in recipients:
                formatted_message = None
                if pref.context.name == 'email':
                    formatted_message = formatters.email_batch(
                        [m['body'] for m in messages], recipient)
                elif pref.context.name == 'irc':
                    formatted_message = formatters.irc_batch(
                        [m['body'] for m in messages], recipient)
                if formatted_message is None:
                        _log.error('A batch message for %r was not formatted, skipping!',
                                   recipient)
                        continue

                backend_message = {
                    "context": pref.context.name,
                    "recipient": recipient,
                    "fedmsg": messages,
                    "formatted_message": formatted_message,
                }
                routing_key = BACKEND_QUEUE_PREFIX + pref.context.name
                producer.publish(backend_message, routing_key=routing_key,
                                 declare=[Queue(routing_key, durable=True)])

            for message in queued_messages:
                message.dequeue(session)
            session.commit()


def _batch_ready(preference):
    """
    Determine if a message batch is ready for a user.

    Args:
        preference (models.Preference): The user preference entry which
            contains the user's batch preferences.
    Returns:
        bool: True if there's a batch ready.
    """
    session = models.Session()
    count = models.QueuedMessage.count_for(session, preference.user, preference.context)
    if not count:
        return False

    # Batch based on count
    if preference.batch_count is not None and preference.batch_count <= count:
        _log.info("Sending digest for %r per msg count", preference.user.openid)
        return True

    # Batch based on time
    earliest = models.QueuedMessage.earliest_for(
        session, preference.user, preference.context)
    now = datetime.datetime.utcnow()
    delta = datetime.timedelta.total_seconds(now - earliest.created_on)
    if preference.batch_delta is not None and preference.batch_delta <= delta:
        _log.info("Sending digest for %r per time delta", preference.user.openid)
        return True

    return False


@app.task(name='fmn.tasks.heat_fas_cache', ignore_results=True)
def heat_fas_cache():  # pragma: no cover
    """
    Fetch all users from FAS and populate the local Redis cache.

    This is helpful to do once on startup since we'll need everyone's email or
    IRC nickname eventually.
    """
    fmn_fasshim.make_fas_cache(**config.app_conf)


@app.task(name='fmn.tasks.confirmations', ignore_results=True)
def confirmations():
    """
    Load all pending confirmations, create formatted messages, and dispatch them to the
    delivery service.

    This is intended to be dispatched regularly via celery beat.
    """
    session = models.Session()
    models.Confirmation.delete_expired(session)
    pending = models.Confirmation.query.filter_by(status='pending').all()
    broker_url = config.app_conf['celery']['broker']
    with connections[Connection(broker_url)].acquire(block=True, timeout=60) as conn:
        producer = conn.Producer()
        for confirmation in pending:
            message = None
            if confirmation.context.name == 'email':
                message = formatters.email_confirmation(confirmation)
            else:
                # The way the irc backend is currently written, it has to format the
                # confirmation itself. For now, just send an empty message, but in the
                # future it may be worth refactoring the irc backend to let us format here.
                message = ''
            recipient = {
                confirmation.context.detail_name: confirmation.detail_value,
                'user': confirmation.user.openid,
                'triggered_by_links': False,
                'confirmation': True,
            }
            backend_message = {
                "context": confirmation.context.name,
                "recipient": recipient,
                "fedmsg": {},
                "formatted_message": message,
            }
            _log.info('Dispatching confirmation message for %r', confirmation)
            confirmation.set_status(session, 'valid')
            routing_key = BACKEND_QUEUE_PREFIX + confirmation.context.name
            producer.publish(backend_message, routing_key=routing_key,
                             declare=[Queue(routing_key, durable=True)])


#: A Celery task that accepts a message as input and determines the recipients.
find_recipients = app.tasks[_FindRecipients.name]
