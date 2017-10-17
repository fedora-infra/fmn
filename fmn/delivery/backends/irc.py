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
import logging

from bleach import clean
from twisted.internet import ssl, reactor
import twisted.internet.protocol
import twisted.words.protocols.irc

from fmn import formatters
from fmn.exceptions import FmnError
from .base import BaseBackend
import fmn.lib.models

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


HELP_TEMPLATE = """
I am a notifications bot run by Fedora Infrastructure.  My commands are:
  'stop'  -- stops all messages
  'start' -- starts sending messages again
  'list categories' -- list all the categories
  'list rules <category_name>' -- list all the rules for a category
  'list filters' -- list all filters for sender's nick
  'list filters <filter_name>' -- list all the rules for the filter
  'help'  -- produces this help message
You can update your preferences at {base_url}
You can contact {support_email} if you have any concerns/issues/abuse.
"""

rule_template = """
 - {rule_title}
   {rule_doc}
"""


class IRCBackend(BaseBackend):
    __context_name__ = 'irc'

    def __init__(self, *args, **kwargs):
        super(IRCBackend, self).__init__(*args, **kwargs)
        self.network = self.config['fmn.irc.network']
        self.nickname = self.config['fmn.irc.nickname']
        self.nickserv_pass = self.config.get('fmn.irc.nickserv_pass')
        self.use_ssl = self.config.get('fmn.irc.use_ssl', False)
        self.port = int(self.config['fmn.irc.port'])
        self.timeout = int(self.config['fmn.irc.timeout'])

        self.clients = []
        factory = IRCClientFactory(self)

        # These are callbacks we use when people try to message us.
        self.commands = {
            'start': self.cmd_start,
            'stop': self.cmd_stop,
            'list': self.cmd_list,
            'help': self.cmd_help,
            'default': self.cmd_default,
        }

        # These are callbacks we use when people try to message us with
        # arguments for the `list` commands e.g. list categories,
        # list filters etc.
        self.list_commands = {
            'categories': self.subcmd_categories,
            'rules': self.subcmd_rules,
            'filters': self.subcmd_filters,
        }

        if self.use_ssl:
            log.info('Connecting to IRC server %s:%s with TLS', self.network, self.port)
            reactor.connectSSL(
                self.network,
                self.port,
                factory,
                ssl.ClientContextFactory(),
                timeout=self.timeout,
            )
        else:
            log.info('Connecting to IRC server %s:%s', self.network, self.port)
            reactor.connectTCP(
                self.network,
                self.port,
                factory,
                timeout=self.timeout,
            )

    def get_preference(self, session, detail_value):
        return self.preference_for(session, detail_value)

    def dequote(self, text):
        """ Remove the beginning and the ending matching single
        and double quotes. Returns unchanged string if beginning and
        ending character don't match.

        :args text: text in which the quotes need to removed.
        """
        if text and (text[0] == text[-1]) and text.startswith(("'", '"')):
            return text[1:-1]
        return text

    def send(self, nick, line):
        for client in self.clients:
            client.msg(nick.encode('utf-8'), line.encode('utf-8'))

    def cmd_start(self, nick, message):
        log.info("CMD start: %r sent us %r" % (nick, message))
        sess = fmn.lib.models.init(self.config.get('fmn.sqlalchemy.uri'))
        if self.disabled_for(sess, nick):
            self.enable(sess, nick)
            self.send(nick, "OK")
        else:
            self.send(nick, "Messages not currently stopped.  Nothing to do.")
        sess.commit()
        sess.close()

    def cmd_stop(self, nick, message):
        log.info("CMD stop:  %r sent us %r" % (nick, message))
        sess = fmn.lib.models.init(self.config.get('fmn.sqlalchemy.uri'))

        if self.disabled_for(sess, nick):
            self.send(nick, "Messages already stopped.  Nothing to do.")
        else:
            self.disable(sess, nick)
            self.send(nick, "OK")
        sess.commit()
        sess.close()

    def cmd_list(self, nick, message):
        log.info("CMD list:  %r sent us %r" % (nick, message))
        if message.strip() == 'list':
            self.commands['default'](nick, message)
        else:
            subcmd_string = message.split(None, 2)[1].strip().lower()
            self.list_commands.get(
                subcmd_string,
                self.commands['default']
            )(nick, message)

    def subcmd_categories(self, nick, message):
        log.info("CMD list categories:  %r sent us %r" % (nick, message))

        valid_paths = fmn.lib.load_rules(root="fmn.rules")
        subcmd_string = message.split(None, 2)[-1].lower()

        # Check if the sub command is `categories` then it returns
        # the list of categories else returns the default error message
        if subcmd_string.strip() == 'categories':

            rule_types = list(set([
                d[path]['submodule'] for _, d in valid_paths.items()
                for path in d
            ]))

            if rule_types:
                self.send(nick, "The list of categories are:")

            for rule_type in rule_types:
                self.send(nick, "  - {rule_type}".format(rule_type=rule_type))

        else:
            self.commands['default'](nick, message)

    def subcmd_rules(self, nick, message):
        log.info("CMD list rules:  %r sent us %r" % (nick, message))

        valid_paths = fmn.lib.load_rules(root="fmn.rules")
        subcmd_string = message.split(None, 2)[-1].lower()

        # Returns the default error message if the rule is not in the format
        # of `list rules <category_name>`
        if subcmd_string.strip() == 'rules':
            self.commands['default'](nick, message)
            return

        # Returns the list of rules associated with the category name
        # else an error message is returned
        valid_category = False
        for root in valid_paths:
            for path in valid_paths[root]:
                if valid_paths[root][path]['submodule'] != subcmd_string:
                    continue
                self.send(nick, '  - {title}'.format(
                    title=valid_paths[root][path]['title']))
                valid_category = True

        if not valid_category:
            self.send(nick, "Not a valid category.")

    def subcmd_filters(self, nick, message):
        log.info("CMD list filters:  %r sent us %r" % (nick, message))

        valid_paths = fmn.lib.load_rules(root="fmn.rules")
        sess = fmn.lib.models.init(self.config.get('fmn.sqlalchemy.uri'))
        pref = self.get_preference(sess, nick)

        if pref is None:
            self.send(nick,
                      'The nick is not configured with Fedora Notifications')
            sess.close()
            return

        subcmd_string = message.split(None, 2)[-1].lower()

        # Returns the list of filters associated with the rule if the sub
        # command ends with `filters` else it is checked for the validity of
        # the filter name. If the matching filter is found then the list of
        # rules for the filter is returned. If the matching filter is not found
        # then an error message is returned
        if subcmd_string.strip() == 'filters':
            filters = pref.filters

            self.send(nick, 'You have {num_filter} filter(s)'.format(
                num_filter=len(filters)))

            for filtr in filters:
                self.send(nick, '  - {filtr_name}'.format(
                    filtr_name=filtr.name)
                )
        else:
            subcmd_string = self.dequote(subcmd_string)

            try:
                filtr = pref.get_filter_name(sess, subcmd_string)
            except ValueError:
                self.send(nick, 'Not a valid filter')
                sess.close()
                return

            rules = filtr.rules
            self.send(nick,
                      '{num_rule} matching rules for this filter'.format(
                        num_rule=len(rules)))

            for rule in rules:
                rule_title = rule.title(valid_paths)
                rule_doc = clean(rule.doc(
                                valid_paths,
                                no_links=True
                            ).replace('\n', ' '), strip=True)
                self.send(nick, rule_template.format(
                    rule_title=rule_title,
                    rule_doc=rule_doc
                ))

                if rule.arguments:
                    for key, value in rule.arguments.iteritems():
                        self.send(nick, '   {key} - {value}'.format(
                            key=key,
                            value=value
                        ))
                self.send(nick, '-*'*10)
        sess.close()

    def cmd_help(self, nick, message):
        log.info("CMD help:  %r sent us %r" % (nick, message))

        lines = self.config.get('fmn.irc_help_template', HELP_TEMPLATE).format(
            support_email=self.config['fmn.support_email'],
            base_url=self.config['fmn.base_url'],
        ).strip().split('\n')

        for line in lines:
            self.send(nick, line)

    def cmd_default(self, nick, message):

        # Ignore notices from freenode services
        if message.startswith('***'):
            return

        log.info("CMD unk:   %r sent us %r" % (nick, message))
        self.send(nick, "say 'help' for help or 'stop' to stop messages")

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
        if recipient.get('confirmation'):
            self._handle_confirmation(recipient['irc nick'])
            return

        session = fmn.lib.models.Session()

        if not self.clients:
            # This is usually the case if we are suffering a netsplit.
            # Raising an exception will cause the message to be requeued and
            # tried again later.
            raise FmnError("IRCBackend has no clients to work with.")

        log.debug("Notifying via irc %r" % recipient)

        if 'irc nick' not in recipient:
            log.warning("No irc nick found.  Bailing.")
            return

        nickname = recipient['irc nick']

        if self.disabled_for(session, detail_value=nickname):
            log.debug("Messages stopped for %r, not sending." % nickname)
            return

        for client in self.clients:
            getattr(client, recipient.get('method', 'msg'))(
                nickname.encode('utf-8'),
                formatted_message.encode('utf-8'),
            )

    def _handle_confirmation(self, nick):
        """
        Dispatch a message to nickserv to make sure the account is registered.

        The "noticed" callback on the client will handle the response.
        """
        if not self.clients:
            log.warning("IRCBackend has no clients to work with.")
            return

        log.debug("Handling confirmation via irc for %r" % nick)

        query = "ACC %s" % nick
        for client in self.clients:
            client.msg((u'NickServ').encode('utf-8'), query.encode('utf-8'))

    def handle_confirmation_valid_nick(self, session, nick):
        if not self.clients:
            log.warning("IRCBackend has no clients to work with.")
            return

        confirmations = fmn.lib.models.Confirmation.by_detail(
            session, context="irc", value=nick)

        for confirmation in confirmations:
            lines = formatters.irc_confirmation(confirmation).split('\n')
            for line in lines:
                for client in self.clients:
                    client.msg(nick.encode('utf-8'), line.encode('utf-8'))

    def handle_confirmation_invalid_nick(self, session, nick):
        confirmations = fmn.lib.models.Confirmation.by_detail(
            session, context="irc", value=nick)
        for confirmation in confirmations:
            confirmation.set_status(session, 'invalid')

    def cleanup_clients(self, factory):
        self.clients = [c for c in self.clients if c.factory != factory]

    def add_client(self, client):
        self.clients.append(client)


class IRCBackendProtocol(twisted.words.protocols.irc.IRCClient):
    lineRate = 0.6
    sourceURL = "http://github.com/fedora-infra/fmn"

    @property
    def nickname(self):
        return self.factory.parent.nickname

    @property
    def log(self):
        return self.factory.parent.log

    @property
    def commands(self):
        return self.factory.parent.commands

    def signedOn(self):
        log.info("Signed on as %r." % self.nickname)
        # Attach ourselves back on the consumer to be used.
        self.factory.parent.add_client(self)
        if self.factory.parent.nickname and self.factory.parent.nickserv_pass:
            log.info('Identifying with NickServ as %s', self.nickname)
            self.msg('NickServ', 'IDENTIFY {nick} {password}'.format(
                nick=self.factory.parent.nickname, password=self.factory.parent.nickserv_pass))

    def privmsg(self, user, channel, msg):
        """ Called when a user privmsgs me. """
        return self.noticed(user, channel, msg)

    def noticed(self, user, channel, msg):
        """ Called when I have a notice from a user. """
        self.factory.parent.log.debug(
            "Received notice %r %r %r" % (user, channel, msg))

        # We query NickServ off the bat.  This is probably her responding.
        # We check NickServ before doing confirmations, so, let's do that now.
        if user == "NickServ!NickServ@services.":
            nick, commands, result = msg.split(None, 2)

            uri = self.factory.parent.config.get('fmn.sqlalchemy.uri')
            s = fmn.lib.models.init(uri)

            if result.strip() == '3':
                # Then all is good.
                # 1) the nickname is registered
                # 2) the person is currently logged in and identified.
                self.factory.parent.handle_confirmation_valid_nick(s, nick)
            else:
                # Something is off.  There are a number of possible scenarios,
                # but we'll just report back "invalid"
                self.factory.parent.handle_confirmation_invalid_nick(s, nick)

            s.commit()
            s.close()
        else:
            # If it's not NickServ, then it might be a user asking for help
            nick = user.split("!")[0]
            cmd_string = msg.split(None, 1)[0].lower()
            self.commands.get(cmd_string, self.commands['default'])(nick, msg)


class IRCClientFactory(twisted.internet.protocol.ClientFactory):
    protocol = IRCBackendProtocol

    def __init__(self, parent):
        self.parent = parent

    def clientConnectionLost(self, connector, reason):
        self.parent.cleanup_clients(factory=self)

        if self.parent.die:
            self.parent.log.warning("Lost IRC connection.  Shutting down.")
            return

        self.parent.log.warning("Lost connection %r, reconnecting." % reason)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        self.parent.cleanup_clients(factory=self)

        if self.parent.die:
            self.parent.log.warning("Couldn't connect to IRC.  Shutting down.")
            return

        self.parent.log.error("Could not connect: %r, retry in 60s" % reason)
        reactor.callLater(60, connector.connect)
