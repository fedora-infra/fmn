from fmn.consumer.backends.base import BaseBackend
import fedmsg.meta

import twisted.internet.protocol
import twisted.words.protocols.irc

from twisted.internet import reactor


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
        message = fedmsg.meta.msg2repr(msg, **self.config)

        for client in self.clients:
            getattr(client, recipient['method'])(
                recipient['ircnick'].encode('utf-8'),
                message.encode('utf-8'),
            )

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
