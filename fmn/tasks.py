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

from celery.utils.log import get_task_logger
from fedmsg_meta_fedora_infrastructure import fasshim
from kombu import Connection, Queue
from kombu.pools import connections
from celery import task
import fedmsg
import fedmsg.meta
import fedmsg_meta_fedora_infrastructure

from . import config, lib as fmn_lib
from .celery import app
from . import fmn_fasshim


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
        self.config = fedmsg.config.load_config()
        fedmsg.meta.make_processors(**self.config)
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
             self.user_preferences, message_body, self.valid_paths, self.config)
        _log.info('Found %s recipients for message %s', sum(map(len, results.values())), topic)

        broker_url = config.app_conf['celery']['broker']
        with connections[Connection(broker_url)].acquire(block=True, timeout=60) as conn:
            producer = conn.Producer()
            for context, recipients in results.items():
                _log.info('Publishing recipients list for the %s backend', context)
                producer.publish(
                    {'context': context, 'recipients': recipients, 'raw_msg': message},
                    routing_key='backends',
                    declare=[Queue('backends', durable=True)],
                )


#: A Celery task that accepts a message as input and determines the recipients.
find_recipients = app.tasks[_FindRecipients.name]
