import abc
import logging

import requests

import fmn.lib.models


log = logging.getLogger(__name__)


def shorten(link):
    if not link:
        return ''
    try:
        response = requests.get('http://da.gd/s', params=dict(url=link))
        return response.text.strip()
    except Exception as e:
        log.warn("Link shortening failed: %r" % e)
        return link


class BaseBackend(object):
    __metaclass__ = abc.ABCMeta
    die = False

    def __init__(self, config, **kwargs):
        self.config = config
        self.log = logging.getLogger("fmn")

    # Some methods that must be implemented by backends.
    @abc.abstractmethod
    def handle(self, session, recipient, msg, streamline=False):
        """
        Handle sending a single message to one recipient.

        :param session:     The SQLAlchemy database session to use.
        :type  session:     sqlalchemy.orm.session.Session
        :param recipient:   The recipient of the message and their settings.
        :type recipient:    dict
        :param msg:         The message to send to the user.
        :type  msg:         dict
        :param streamline:  ?
        :param streamline:  boolean
        """
        pass

    @abc.abstractmethod
    def handle_batch(self, session, messages):
        """
        Handle sending a set of one or more messages to one recipient.

        :param session:     The SQLAlchemy database session to use.
        :type  session:     sqlalchemy.orm.session.Session
        :param recipient:   The recipient of the messages and their settings.
        :type recipient:    dict
        :param msg:         The messages to send to the user.
        :type  msg:         dict
        """
        pass

    @abc.abstractmethod
    def handle_confirmation(self, session, confirmation):
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
