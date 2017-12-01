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
Formatters for message backends.

These take raw fedmsgs and produce human-readable notifications as text. This
text is then passed to a delivery backend and sent to the user.
"""
from __future__ import absolute_import

import logging
import json
import uuid
import datetime
import time
import email as email_module

import arrow
import requests
import six
import pytz
import fedmsg.meta

from . import config

_log = logging.getLogger(__name__)


EMAIL_CONFIRMATION_TEMPLATE = u"""
{username} has requested that notifications be sent to this email address
* To accept, visit this address:
  {acceptance_url}
* Or, to reject you can visit this address:
  {rejection_url}
Alternatively, you can ignore this.  This is an automated message, please
email {support_email} if you have any concerns/issues/abuse.
"""

IRC_CONFIRMATION_TEMPLATE = u"""
{username} has requested that notifications be sent to this nick
* To accept, visit this address:
  {acceptance_url}
* Or, to reject you can visit this address:
  {rejection_url}
Alternatively, you can ignore this.  This is an automated message, please
email {support_email} if you have any concerns/issues/abuse.
I am run by Fedora Infrastructure.  Type 'help' for more information.
"""

MIRC_COLORS = {
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


def shorten(link):
    """
    Attempt to shorten a link using a shortening service.

    Args:
        link (str): The link to shorten.

    Returns:
        str: The link. If the shortener service was unreachable, the original link is returned.
    """
    if not link:
        return ''
    try:
        response = requests.get('http://da.gd/s', params=dict(url=link), timeout=30)
        return response.text.strip()
    except Exception as e:
        _log.warn("Link shortening failed: %r" % e)
        return link


def irc(message, recipient):
    """
    Format a fedmsg for delivery via IRC.

    Args:
        message (dict): The fedmsg's message body.
        recipient (dict): The recipient's formatting preferences.

    Returns:
        str: A human-readable message suitable for delivery to the user.
    """
    if recipient['markup_messages']:
        template = u"{title} -- {subtitle} {delta} {link} {flt}"
    else:
        template = u"{subtitle} {delta} {link} {flt}"
    title = 'Unknown title'
    subtitle = 'Unknown subtitle'
    link = None
    try:
        title = fedmsg.meta.msg2title(message, **config.app_conf)
    except Exception:
        _log.exception('Unable to produce a message title for %r', message)
    try:
        subtitle = fedmsg.meta.msg2subtitle(message, **config.app_conf)
    except Exception:
        _log.exception('Unable to produce a message subtitle for %r', message)
    try:
        link = fedmsg.meta.msg2link(message, **config.app_conf)
        if recipient['shorten_links']:
            link = shorten(link)
    except Exception:
        _log.exception('Unable to produce a message link for %r', message)

    # Tack a human-readable delta on the end so users know that fmn is
    # backlogged (if it is).
    delta = ''
    if time.time() - message['timestamp'] > 10:
        delta = arrow.get(message['timestamp']).humanize()

    flt = ''
    if recipient['triggered_by_links'] and 'filter_id' in recipient:
        flt_template = "{base_url}{user}/irc/{filter_id}"
        flt_link = flt_template.format(
            base_url=config.app_conf['fmn.base_url'], **recipient)
        if recipient['shorten_links']:
            flt_link = shorten(flt_link)
        flt = "(triggered by %s)" % flt_link

    if recipient['markup_messages']:
        def markup(s, color):
            return "\x03%i%s\x03" % (MIRC_COLORS[color], s)

        color_lookup = config.app_conf.get('irc_color_lookup', {})
        title_color = color_lookup.get(title.split('.')[0], "light grey")
        title = markup(title, title_color)
        if link:
            link = markup(link, "teal")

    return template.format(title=title, subtitle=subtitle, delta=delta,
                           link=link, flt=flt).strip()


def irc_batch(messages, recipient):
    """
    Format a list of messages as a single message summary.

    Args:
        messages (list): A list of dictionaries, where each dictionary is a fedmsg.
        recipient (dict): The message recipient.
    """
    if len(messages) == 1:
        return irc(messages[0], recipient)
    else:
        template = u'{subtitle} {delta} {link} {filter_link}\n'
        formatted_message = u''
        try:
            # This apparently returns a list of dicts with the 'link', 'subtitle',
            # 'subjective', 'secondary_icon' and any number of other keys from the
            # individual conglomerator.
            conglomerated = fedmsg.meta.conglomerate(messages, **config.app_conf)
            for message in conglomerated:
                formatted_message += template.format(
                    subtitle=message['subtitle'], delta=message.get('human_time', ''),
                    link=message['link'], filter_link=_irc_filter_link(recipient))
        except Exception:
            _log.exception('An unexpected error occurred while processing an IRC batch')
            formatted_message = (
                u'You received {} notifications in this batch, but there was a problem '
                u'making them human-readable. This error has been automatically reported. '
                u'Join #fedora-admin for more information. '
                u'The message IDs are: \n').format(len(messages))
            for message in messages:
                if 'msg_id' in message:
                    _log.error('%s was among the batch that could not be processed',
                               message['msg_id'])
                    formatted_message += u'{}\n'.format(message['msg_id'])
        return formatted_message


def _irc_filter_link(recipient):
    """
    Create a link to the recipient's filter that triggered this message.

    Args:
        recipient: The recipient dictionary.
    Returns:
        six.text_type: A (potentially shortened) link to the user's filter or
            an empty string if the user has turned off the setting to include
            links to the triggered filter.
    """
    if recipient['triggered_by_links'] and 'filter_id' in recipient:
        link = u'{base_url}{user}/irc/{filter_id}'.format(
            base_url=config.app_conf['fmn.base_url'], **recipient)
        if recipient['shorten_links']:
            link = shorten(link)
        return link
    return u''


def irc_confirmation(confirmation):
    """
    Create a confirmation irc message to send to new users with a confirmation link.

    Args:
        confirmation (models.Confirmation): The confirmation database entry.

    Returns:
        str: The irc message to send.
    """
    acceptance_url = config.app_conf['fmn.acceptance_url'].format(
        secret=confirmation.secret)
    rejection_url = config.app_conf['fmn.rejection_url'].format(
        secret=confirmation.secret)
    template = config.app_conf.get('fmn.irc_confirmation_template',
                                   IRC_CONFIRMATION_TEMPLATE)
    message = template.format(
        acceptance_url=acceptance_url,
        rejection_url=rejection_url,
        support_email=config.app_conf['fmn.support_email'],
        username=confirmation.openid,
    ).strip()
    return message


def sse(msg, recipient):
    """
    Here we have to distinguish between two different kinds of messages that
    might arrive: the `raw` message from fedmsg itself and the product of a
    call to `fedmsg.meta.conglomerate(..)` by way of ``handle_batch``.

    The format from `fedmsg.meta.conglomerate(..)` should be::

      {
        'subtitle': 'relrod pushed commits to ghc and 487 other packages',
        'link': None,  # This could be something.
        'icon': 'https://that-git-logo',
        'secondary_icon': 'https://that-relrod-avatar',
        'start_time': some_timestamp,
        'end_time': some_other_timestamp,
        'human_time': '5 minutes ago',
        'usernames': ['relrod'],
        'packages': ['ghc', 'nethack', ... ],
        'topics': ['org.fedoraproject.prod.git.receive'],
        'categories': ['git'],
        'msg_ids': {
            '2014-abcde': {
                'subtitle': 'relrod pushed some commits to ghc',
                'title': 'git.receive',
                'link': 'http://...',
                'icon': 'http://...',
            },
            '2014-bcdef': {
                'subtitle': 'relrod pushed some commits to nethack',
                'title': 'git.receive',
                'link': 'http://...',
                'icon': 'http://...',
            },
        },
      }

    We assume that if the ``msg_ids`` key is present, the message is a
    conglomerated message. If this key is not present, the message will
    be handed to ``fedmsg.meta.msg2*`` methods to extract the necessary
    information.

    The formatted message is a dictionary in the following form:

    {
      "dom_id": "d38b2b6c-a3c9-4772-b6aa-0a70a6bee517",
      "date_time": "2008-09-03T20:56:35.450686Z",
      "icon": "https://apps.fedoraproject.org/packages/images/icons/package_128x128.png",
      "link": "https://pagure.io/<repo>/issue/148703615",
      "markup": "<a href="http://example.com/">Marked up message summary</a>",
      "secondary_icon": null,
    }

    :param msg:         The messages to send to the user.
    :type  msg:         dict
    :param recipient:   The recipient of the messages and their settings.
                        This controls what RabbitMQ queue the message ends
                        up in.
    :type recipient:    dict

    :return: A UTF-8-encoded JSON-serialized message.
    :rtype:  bytes
    """
    conglomerated = 'msg_ids' in msg
    dom_id = six.text_type(uuid.uuid4())
    date_time = ''
    icon = ''
    link = ''
    markup = ''
    secondary_icon = ''
    username = ''
    subtitle = ''

    if conglomerated:
        # This handles messages that have already been 'conglomerated'.
        title = ''
        subtitle = msg['subtitle']
        link = msg['link']
    else:
        # This handles normal, 'raw' messages which get passed through msg2*.
        # Tack a human-readable delta on the end so users know that fmn is
        # backlogged (if it is).
        if msg['timestamp']:
            date_time = msg['timestamp']
            date_time = datetime.datetime.fromtimestamp(date_time)
            date_time = date_time.replace(tzinfo=pytz.utc).isoformat()
        else:
            date_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc).isoformat()

        icon = fedmsg.meta.msg2icon(msg, **config.app_conf)
        link = fedmsg.meta.msg2link(msg, **config.app_conf)
        secondary_icon = fedmsg.meta.msg2secondary_icon(msg, **config.app_conf)
        username = fedmsg.meta.msg2agent(msg, **config.app_conf)
        title = fedmsg.meta.msg2title(msg, **config.app_conf)
        subtitle = fedmsg.meta.msg2subtitle(msg, **config.app_conf)

    if recipient['shorten_links']:
        link = shorten(link)
    event_link = ''
    if title and link:
        event_link = '<a href="' + link + '">' + title + '</a>'
    user_link = ''
    if username:
        user_link = '<a href="/' + username.replace("@", "") + '">' + username + '</a>'

    markup = ''
    if user_link:
        markup += user_link
    if event_link:
        markup += ' ' + event_link
    if subtitle:
        markup += ' ' + subtitle
    markup = markup.strip()

    output = {
        'dom_id': dom_id,
        'date_time': date_time,
        'icon': icon,
        'link': link,
        'markup': markup,
        'secondary_icon': secondary_icon
    }

    return json.dumps(output)


def email(message, recipient):
    """
    Create a Python email Message that's ready for delivery.

    This handles setting all the headers and formatting.

    Args:
        message (dict): The fedmsg to turn into an email.
        recipient (dict): A dictionary containing (at a minimum) the
            `email_address` (str) and `triggered_by_links` (bool) keys.

    Returns:
        str: The email as a unicode string.
    """
    email_message = _base_email(recipient=recipient, messages=[message])

    try:
        subject = fedmsg.meta.msg2subtitle(message, **config.app_conf) or u'fedmsg notification'
    except Exception:
        _log.exception('fedmsg.meta.msg2subtitle failed to handle %r', message)
        subject = u'fedmsg notification'
    subject_prefix = config.app_conf.get('fmn.email.subject_prefix', '')
    if subject_prefix:
        subject = u'{0} {1}'.format(
            subject_prefix.strip(), subject.strip())
    email_message.add_header('Subject', subject.encode('utf-8'))

    try:
        content = fedmsg.meta.msg2long_form(message, **config.app_conf) or u''
    except Exception:
        _log.exception('fedmsg.meta.msg2long_form failed to handle %r', message)
        content = json.dumps(message, sort_keys=True, indent=4)

    try:
        link = fedmsg.meta.msg2link(message, **config.app_conf)
        if link:
            content += "\n\t" + link
    except Exception:
        _log.exception('fedmsg.meta.msg2link failed to handle %r', message)

    # Since we do simple text email, adding the footer to the content
    # before setting the payload.
    footer = config.app_conf.get('fmn.email.footer', u'')
    if 'filter_id' in recipient and 'user' in recipient and recipient['triggered_by_links']:
        base_url = config.app_conf['fmn.base_url']
        footer = (u'You received this message due to your preference settings at \n{base_url}'
                  u'{user}/email/{filter_id}').format(base_url=base_url, **recipient) + footer
    if footer:
        content += u'\n\n--\n{0}'.format(footer.strip())
    email_message.set_payload(content.encode('utf-8'), 'utf-8')

    # Explicitly declare encoding, but remove the transfer encoding
    # https://github.com/fedora-infra/fmn/issues/94
    email_message.set_charset('utf-8')

    return email_message.as_string()


def email_batch(messages, recipient):

    if len(messages) == 1:
        return email(messages[0], recipient)

    email_message = _base_email(recipient=recipient, messages=messages)
    email_message.add_header(
        'Subject', u'Fedora Notifications Digest ({n} updates)'.format(n=len(messages)))

    content = u'Digest Summary:\n'
    message_template = u'{number}.\t{summary} ({ts})\n\t- {link}\n{details}{separator}'
    separator = u'\n\n' + '-' * 79 + '\n\n'
    for message_number, message in enumerate(messages, start=1):
        try:
            summary = fedmsg.meta.msg2subtitle(message, **config.app_conf) or u''
        except Exception:
            _log.exception('fedmsg.meta.msg2subtitle failed to handle %r', message)
            summary = u'Unparsable message subtitle'

        if recipient.get('verbose', True):
            try:
                longform = fedmsg.meta.msg2long_form(message, **config.app_conf) or u''
            except Exception:
                _log.exception('fedmsg.meta.msg2long_form failed to handle %r', message)
                longform = u'Unparsable message details'
        else:
            longform = u''

        try:
            link = fedmsg.meta.msg2link(message, **config.app_conf) or u''
        except Exception:
            _log.exception('fedmsg.meta.msg2link failed to handle %r', message)
            link = u'No link could be found in the message'

        timestamp = datetime.datetime.fromtimestamp(message['timestamp'])
        content += message_template.format(
            number=message_number, summary=summary, ts=timestamp.strftime('%c'),
            link=link, details=longform, separator=separator)

    if len(content) > 20000000:
        # This email is enormous, too large to be sent.
        content = (u'This message digest was too large to be sent!\n'
                   u'The following messages were batched:\n\n')
        for msg in messages:
            content += msg['msg_id'] + '\n'

        if len(content) > 20000000:
            # Even the briefest summary is too big
            content = (u'The message digest was so large, not even a summary could be sent.\n'
                       u'Consider adjusting your FMN settings.\n')

    email_message.set_payload(content.encode('utf-8'), 'utf-8')
    return email_message.as_string()


def email_confirmation(confirmation):
    """
    Create a confirmation email to new user emails with a confirmation link.

    Args:
        confirmation (models.Confirmation): The confirmation database entry.

    Returns:
        str: The email to send as a string.
    """
    email_message = _base_email()
    email_message.add_header('To', confirmation.detail_value)
    email_message.add_header('Subject', u'Confirm notification email')
    acceptance_url = config.app_conf['fmn.acceptance_url'].format(
        secret=confirmation.secret)
    rejection_url = config.app_conf['fmn.rejection_url'].format(
        secret=confirmation.secret)
    template = config.app_conf.get('fmn.mail_confirmation_template',
                                   EMAIL_CONFIRMATION_TEMPLATE)
    content = template.format(
        acceptance_url=acceptance_url,
        rejection_url=rejection_url,
        support_email=config.app_conf['fmn.support_email'],
        username=confirmation.openid,
    ).strip()
    email_message.set_payload(content)
    return email_message.as_string()


def _base_email(recipient=None, messages=None):
    """
    Create an email Message with some basic headers to mark the email as auto-generated.

    Returns:
        email.Message.Message: The email message object with the 'Precedence' and 'Auto-Submitted'
            headers set.
    """
    email_message = email_module.Message.Message()
    # Although this is a non-standard header and RFC 2076 discourages it, some
    # old clients don't honour RFC 3834 and will auto-respond unless this is set.
    email_message.add_header('Precedence', 'Bulk')
    # Mark this mail as auto-generated so auto-responders don't respond; see RFC 3834
    email_message.add_header('Auto-Submitted', 'auto-generated')
    email_message.add_header('From', config.app_conf['fmn.email.from_address'].encode('utf-8'))

    if recipient and 'email address' in recipient:
        email_message.add_header('To', recipient['email address'].encode('utf-8'))

    if messages:
        try:
            topics = set([message['topic'] for message in messages])
            for topic in topics:
                email_message.add_header('X-Fedmsg-Topic', topic.encode('utf-8'))
            categories = set([topic.split('.')[3] for topic in topics])
            for cat in categories:
                email_message.add_header('X-Fedmsg-Category', cat.encode('utf-8'))
        except Exception:
            _log.exception('Unable to parse message topic and category for %r', messages)

        for msg in messages:
            try:
                for username in fedmsg.meta.msg2usernames(msg, **config.app_conf) or []:
                    email_message.add_header('X-Fedmsg-Username', username.encode('utf-8'))
            except Exception:
                _log.exception('fedmsg.meta.msg2usernames failed to handle %r', msg)
            try:
                for package in fedmsg.meta.msg2packages(msg, **config.app_conf) or []:
                    email_message.add_header('X-Fedmsg-Package', package.encode('utf-8'))
            except Exception:
                _log.exception('fedmsg.meta.msg2packages failed to handle %r', msg)

    return email_message
