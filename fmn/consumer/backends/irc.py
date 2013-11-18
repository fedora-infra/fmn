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
"""

class IRCBackend(BaseBackend):
    def __init__(self, *args, **kwargs):
        super(IRCBackend, self).__init__(*args, **kwargs)
        self.network = self.config['fmn.irc.network']
        self.nickname = self.config['fmn.irc.nickname']
        self.port = int(self.config['fmn.irc.port'])
        self.timeout = int(self.config['fmn.irc.timeout'])

        self.clients = []
        factory = IRCClientFactory(self)

        reactor.connectTCP(
            self.network,
            self.port,
            factory,
            timeout=self.timeout,
        )

    def handle(self, recipient, msg):
        if not self.clients:
            self.log.warning("IRCBackend has no clients to work with.")
            return

        self.log.debug("Notifying via irc %r" % recipient)

        if 'irc nick' not in recipient:
            self.log.warning("No irc nick found.  Bailing.")
            return

        message = fedmsg.meta.msg2repr(msg, **self.config)

        for client in self.clients:
            getattr(client, recipient.get('method', 'msg'))(
                recipient['irc nick'].encode('utf-8'),
                message.encode('utf-8'),
            )

    def handle_confirmation(self, confirmation):
        if not self.clients:
            self.log.warning("IRCBackend has no clients to work with.")
            return

        self.log.debug("Handling confirmation via irc %r" % confirmation)

        query = "ACC %s" % confirmation.detail_value
        for client in self.clients:
            client.msg((u'NickServ').encode('utf-8'), query.encode('utf-8'))

    def handle_confirmation_valid_nick(self, nick):
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
                username=confirmation.user_name,
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
    sourceURL = "http://github.com/fedora-infra/fedmsg-notifications"

    @property
    def nickname(self):
        return self.factory.parent.nickname

    @property
    def log(self):
        return self.factory.parent.log

    def signedOn(self):
        self.log.info("Signed on as %r." % self.nickname)
        # Attach ourselves back on the consumer to be used.
        self.factory.parent.add_client(self)

    def noticed(self, user, channel, message):
        """ Called when I have a notice from a user. """
        self.factory.parent.log.debug(
            "Received notice %r %r %r" % (user, channel, message))

        # We are only interested in notices from NickServ
        if user != "NickServ!NickServ@services.":
            return

        nickname, commands, result = message.split(None, 2)
        if result.strip() == '3':
            # Then all is good.
            # 1) the nickname is registered
            # 2) the person is currently logged in and identified.
            self.factory.parent.handle_confirmation_valid_nick(nickname)
        else:
            # Something is off.  There are a number of possible scenarios, but
            # we'll just report back "invalid"
            self.factory.parent.handle_confirmation_invalid_nick(nickname)


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
