import fmn.lib.models
from fmn.consumer.backends.base import BaseBackend
import fedmsg.meta

import twisted.internet.protocol
import twisted.words.protocols.irc

from twisted.internet import reactor

confirmation_template = """
{username} has requested that notifications be sent to this nick
* To accept, visit this address:
  {acceptance_url}
* Or, to reject you can visit this address:
  {rejection_url}
Alternatively, you can ignore this.  This is an automated message, please
email {support_email} if you have any concerns/issues/abuse.
I am run by Fedora Infrastructure.  Type 'help' for more information.
"""

help_template = """
I am a notifications bot run by Fedora Infrastructure.  My commands are:
  'stop'  -- stops all messages
  'start' -- starts sending messages again
  'help'  -- produces this help message
You can update your preferences at {base_url}
You can contact {support_email} if you have any concerns/issues/abuse.
"""


class IRCBackend(BaseBackend):
    __context_name__ = 'irc'

    def __init__(self, *args, **kwargs):
        super(IRCBackend, self).__init__(*args, **kwargs)
        self.network = self.config['fmn.irc.network']
        self.nickname = self.config['fmn.irc.nickname']
        self.port = int(self.config['fmn.irc.port'])
        self.timeout = int(self.config['fmn.irc.timeout'])

        self.clients = []
        factory = IRCClientFactory(self)

        # These are callbacks we use when people try to message us.
        self.commands = {
            'start': self.cmd_start,
            'stop': self.cmd_stop,
            'help': self.cmd_help,
            'default': self.cmd_default,
        }

        reactor.connectTCP(
            self.network,
            self.port,
            factory,
            timeout=self.timeout,
        )

    def send(self, nick, line):
        for client in self.clients:
            client.msg(nick.encode('utf-8'), line.encode('utf-8'))

    def cmd_start(self, nick, message):
        self.log.info("CMD start: %r sent us %r" % (nick, message))
        if self.disabled_for(nick):
            self.enable(nick)
            self.send(nick, "OK")
        else:
            self.send(nick, "Messages not currently stopped.  Nothing to do.")

    def cmd_stop(self, nick, message):
        self.log.info("CMD stop:  %r sent us %r" % (nick, message))
        if self.disabled_for(nick):
            self.send(nick, "Messages already stopped.  Nothing to do.")
        else:
            self.disable(nick)
            self.send(nick, "OK")

    def cmd_help(self, nick, message):
        self.log.info("CMD help:  %r sent us %r" % (nick, message))

        lines = help_template.format(
            support_email=self.config['fmn.support_email'],
            base_url=self.config['fmn.base_url'],
        ).strip().split('\n')

        for line in lines:
            self.send(nick, line)

    def cmd_default(self, nick, message):

        # Ignore notices from freenode services
        if message.startswith('***'):
            return

        self.log.info("CMD unk:   %r sent us %r" % (nick, message))
        self.send(nick, "say 'help' for help or 'stop' to stop messages")

    def handle(self, recipient, msg):
        if not self.clients:
            self.log.warning("IRCBackend has no clients to work with.")
            return

        self.log.debug("Notifying via irc %r" % recipient)

        if 'irc nick' not in recipient:
            self.log.warning("No irc nick found.  Bailing.")
            return

        message = fedmsg.meta.msg2repr(msg, **self.config)

        nickname = recipient['irc nick']

        if self.disabled_for(detail_value=nickname):
            self.log.debug("Messages stopped for %r, not sending." % nickname)
            return

        for client in self.clients:
            getattr(client, recipient.get('method', 'msg'))(
                nickname.encode('utf-8'),
                message.encode('utf-8'),
            )

    def handle_batch(self, recipient, queued_messages):
        for queued_message in queued_messages:
            self.handle(recipient, queued_message.message)

    def handle_confirmation(self, confirmation):
        if not self.clients:
            self.log.warning("IRCBackend has no clients to work with.")
            return

        self.log.debug("Handling confirmation via irc %r" % confirmation)

        query = "ACC %s" % confirmation.detail_value
        for client in self.clients:
            client.msg((u'NickServ').encode('utf-8'), query.encode('utf-8'))

    def handle_confirmation_valid_nick(self, nick):
        if not self.clients:
            self.log.warning("IRCBackend has no clients to work with.")
            return

        confirmations = fmn.lib.models.Confirmation.by_detail(
            self.session, context="irc", value=nick)

        for confirmation in confirmations:
            confirmation.set_status(self.session, 'valid')
            acceptance_url = self.config['fmn.acceptance_url'].format(
                secret=confirmation.secret)
            rejection_url = self.config['fmn.rejection_url'].format(
                secret=confirmation.secret)

            lines = confirmation_template.format(
                acceptance_url=acceptance_url,
                rejection_url=rejection_url,
                support_email=self.config['fmn.support_email'],
                username=confirmation.openid,
            ).strip().split('\n')

            for line in lines:
                for client in self.clients:
                    client.msg(nick.encode('utf-8'), line.encode('utf-8'))

    def handle_confirmation_invalid_nick(self, nick):
        confirmations = fmn.lib.models.Confirmation.by_detail(
            self.session, context="irc", value=nick)
        for confirmation in confirmations:
            confirmation.set_status(self.session, 'invalid')

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
        self.log.info("Signed on as %r." % self.nickname)
        # Attach ourselves back on the consumer to be used.
        self.factory.parent.add_client(self)

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
            nickname, commands, result = msg.split(None, 2)
            if result.strip() == '3':
                # Then all is good.
                # 1) the nickname is registered
                # 2) the person is currently logged in and identified.
                self.factory.parent.handle_confirmation_valid_nick(nickname)
            else:
                # Something is off.  There are a number of possible scenarios,
                # but we'll just report back "invalid"
                self.factory.parent.handle_confirmation_invalid_nick(nickname)
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
        self.parent.log.warning("Lost connection %r, reconnecting." % reason)
        self.parent.cleanup_clients(factory=self)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        self.parent.log.error("Could not connect: %r" % reason)
