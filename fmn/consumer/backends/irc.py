import fmn.lib.models
from fmn.consumer.backends.base import BaseBackend, shorten
import fedmsg.meta

import arrow
import time

import twisted.internet.protocol
import twisted.words.protocols.irc

from twisted.internet import reactor
from bleach import clean

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("fedmsg")


CONFIRMATION_TEMPLATE = """
{username} has requested that notifications be sent to this nick
* To accept, visit this address:
  {acceptance_url}
* Or, to reject you can visit this address:
  {rejection_url}
Alternatively, you can ignore this.  This is an automated message, please
email {support_email} if you have any concerns/issues/abuse.
I am run by Fedora Infrastructure.  Type 'help' for more information.
"""

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

mirc_colors = {
    "white": 0,
    "black": 1,
    "blue": 2,
    "green": 3,
    "red": 4,
    "brown": 5,
    "purple": 6,
    "orange": 7,
    "yellow": 8,
    "light green": 9,
    "teal": 10,
    "light cyan": 11,
    "light blue": 12,
    "pink": 13,
    "grey": 14,
    "light grey": 15,
}


def _format_message(msg, recipient, config):
    # Here we have to distinguish between two different kinds of messages that
    # might arrive: the `raw` message from fedmsg itself and the product of a
    # call to `fedmsg.meta.conglomerate(..)`
    if 'subtitle' not in msg:
        # This handles normal, 'raw' messages which get passed through msg2*.
        title = fedmsg.meta.msg2title(msg, **config)
        subtitle = fedmsg.meta.msg2subtitle(msg, **config)
        link = fedmsg.meta.msg2link(msg, **config)
        # Only prefix with topic if we're "marking up" messages.
        if recipient['markup_messages']:
            template = u"{title} -- {subtitle} {delta}{link}{flt}"
        else:
            template = u"{subtitle} {delta}{link}{flt}"
    else:
        # This handles messages that have already been 'conglomerated'.
        title = u""
        subtitle = msg['subtitle']
        link = msg['link']
        template = u"{subtitle} {delta}{link}{flt}"

    if recipient['shorten_links']:
        link = shorten(link)

    # Tack a human-readable delta on the end so users know that fmn is
    # backlogged (if it is).
    delta = ''
    if time.time() - msg['timestamp'] > 10:
        delta = arrow.get(msg['timestamp']).humanize() + ' '

    flt = ''
    if recipient['triggered_by_links'] and 'filter_id' in recipient:
        flt_template = "{base_url}{user}/irc/{filter_id}"
        flt_link = flt_template.format(
            base_url=config['fmn.base_url'], **recipient)
        if recipient['shorten_links']:
            flt_link = shorten(flt_link)
        flt = "    ( triggered by %s )" % flt_link

    if recipient['markup_messages']:
        def markup(s, color):
            return "\x03%i%s\x03" % (mirc_colors[color], s)

        color_lookup = config.get('irc_color_lookup', {})
        title_color = color_lookup.get(title.split('.')[0], "light grey")
        title = markup(title, title_color)
        if link:
            link = markup(link, "teal")

    return template.format(title=title, subtitle=subtitle, delta=delta,
                           link=link, flt=flt)


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
        self.log.info("CMD start: %r sent us %r" % (nick, message))
        sess = fmn.lib.models.init(self.config.get('fmn.sqlalchemy.uri'))
        if self.disabled_for(sess, nick):
            self.enable(sess, nick)
            self.send(nick, "OK")
        else:
            self.send(nick, "Messages not currently stopped.  Nothing to do.")
        sess.commit()
        sess.close()

    def cmd_stop(self, nick, message):
        self.log.info("CMD stop:  %r sent us %r" % (nick, message))
        sess = fmn.lib.models.init(self.config.get('fmn.sqlalchemy.uri'))

        if self.disabled_for(sess, nick):
            self.send(nick, "Messages already stopped.  Nothing to do.")
        else:
            self.disable(sess, nick)
            self.send(nick, "OK")
        sess.commit()
        sess.close()

    def cmd_list(self, nick, message):
        self.log.info("CMD list:  %r sent us %r" % (nick, message))
        if message.strip() == 'list':
            self.commands['default'](nick, message)
        else:
            subcmd_string = message.split(None, 2)[1].strip().lower()
            self.list_commands.get(
                subcmd_string,
                self.commands['default']
            )(nick, message)

    def subcmd_categories(self, nick, message):
        self.log.info("CMD list categories:  %r sent us %r" % (nick, message))

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
        self.log.info("CMD list rules:  %r sent us %r" % (nick, message))

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
        self.log.info("CMD list filters:  %r sent us %r" % (nick, message))

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
        self.log.info("CMD help:  %r sent us %r" % (nick, message))

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

        self.log.info("CMD unk:   %r sent us %r" % (nick, message))
        self.send(nick, "say 'help' for help or 'stop' to stop messages")

    def handle(self, session, recipient, msg, streamline=False):
        user = recipient['user']

        if not self.clients:
            # This is usually the case if we are suffering a netsplit.
            self.log.warning("IRCBackend has no clients to work with; enqueue")
            fmn.lib.models.QueuedMessage.enqueue(
                session, user, 'irc', msg)
            return

        self.log.debug("Notifying via irc %r" % recipient)

        if 'irc nick' not in recipient:
            self.log.warning("No irc nick found.  Bailing.")
            return

        # Handle any backlog that may have accumulated while we were suffering
        # a netsplit.
        preference_obj = fmn.lib.models.Preference.load(session, user, 'irc')
        if not streamline:
            fmn.consumer.producer.DigestProducer.manage_batch(
                session, self, preference_obj)

        # With all of that out of the way, now we can actually send them the
        # message that triggered all this.
        message = _format_message(msg, recipient, self.config)

        nickname = recipient['irc nick']

        if self.disabled_for(session, detail_value=nickname):
            self.log.debug("Messages stopped for %r, not sending." % nickname)
            return

        for client in self.clients:
            getattr(client, recipient.get('method', 'msg'))(
                nickname.encode('utf-8'),
                message.encode('utf-8'),
            )

    def handle_batch(self, session, recipient, messages):
        # Squash some messages into one conglomerate message
        # https://github.com/fedora-infra/datagrepper/issues/132
        messages = fedmsg.meta.conglomerate(messages, **self.config)
        for message in messages:
            self.handle(session, recipient, message, streamline=True)

    def handle_confirmation(self, session, confirmation):
        if not self.clients:
            self.log.warning("IRCBackend has no clients to work with.")
            return

        self.log.debug("Handling confirmation via irc %r" % confirmation)

        query = "ACC %s" % confirmation.detail_value
        for client in self.clients:
            client.msg((u'NickServ').encode('utf-8'), query.encode('utf-8'))

    def handle_confirmation_valid_nick(self, session, nick):
        if not self.clients:
            self.log.warning("IRCBackend has no clients to work with.")
            return

        confirmations = fmn.lib.models.Confirmation.by_detail(
            session, context="irc", value=nick)

        for confirmation in confirmations:
            confirmation.set_status(session, 'valid')
            acceptance_url = self.config['fmn.acceptance_url'].format(
                secret=confirmation.secret)
            rejection_url = self.config['fmn.rejection_url'].format(
                secret=confirmation.secret)

            template = self.config.get('fmn.irc_confirmation_template',
                                       CONFIRMATION_TEMPLATE)
            lines = template.format(
                acceptance_url=acceptance_url,
                rejection_url=rejection_url,
                support_email=self.config['fmn.support_email'],
                username=confirmation.openid,
            ).strip().split('\n')

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
