import fedora.client

import logging
log = logging.getLogger("fmn")


def new_packager(topic, msg):
    """ Returns a username if the message is about a new packager in FAS. """
    if '.fas.group.member.sponsor' in topic:
        group = msg['msg']['group']
        if group == 'packager':
            return msg['msg']['user']
    return None


def new_badges_user(topic, msg):
    """ Returns a username if the message is about a new fedbadges user. """
    if '.fedbadges.person.login.first' in topic:
        return msg['msg']['user']['username']
    return None


def get_fas_email(config, username):
    """ Return FAS email associated with a username.

    We use this to try and get the right email for new autocreated users.
    We used to just use $USERNAME@fp.o, but when first created most users don't
    have that alias available yet.
    """
    try:
        fas = fedora.client.AccountSystem(**config['fas_credentials'])
        person = fas.person_by_username(username)
        if person.get('email'):
            return person['email']
        raise ValueError("No email found: %r" % username)
    except Exception:
        log.exception("Failed to get FAS email for %r" % username)
        return '%s@fedoraproject.org' % username
