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

import abc
import logging

import fmn.lib.models


log = logging.getLogger(__name__)


class BaseBackend(object):
    """
    The base class for backends.

    .. note:: Many of the methods and attributes in this class are unused and
        need to be factored out.
    """
    __metaclass__ = abc.ABCMeta
    die = False

    def __init__(self, config, **kwargs):
        self.config = config
        self.log = logging.getLogger("fmn")

    # Some methods that must be implemented by backends.
    @abc.abstractmethod
    def deliver(self, formatted_message, recipient, raw_fedmsg):
        """
        Deliver a message to the recipient.

        .. warning::
            Although the original fedmsg is provided, be very careful when making
            use of it. The format will change from message to message, and schema
            changes are common.

        Args:
            formatted_message (str): The formatted message that is ready for delivery
                to the user. It has been formatted according to the user's preferences.
            recipient (dict): The recipient of the message.
            raw_fedmsg (dict): The original fedmsg that was used to produce the formatted
                message.
        """
        pass

    # Some helper methods for our child classes.
    def context_object(self, session):
        return fmn.lib.models.Context.get(self.__context_name__)

    def preference_for(self, session, detail_value):
        return fmn.lib.models.Preference.by_detail(session, detail_value)

    def disabled_for(self, session, detail_value):
        pref = self.preference_for(session, detail_value)

        if not pref:
            return False

        return not pref.enabled

    def enable(self, session, detail_value):
        self.preference_for(session, detail_value).set_enabled(session, True)

    def disable(self, session, detail_value):
        self.preference_for(session, detail_value).set_enabled(session, False)

    def stop(self):
        self.die = True
