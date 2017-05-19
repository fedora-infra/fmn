from __future__ import print_function

import logging
import socket
import string

import fedmsg
import fedmsg.meta
import fedora.client
import fedora.client.fas2
from dogpile.cache import make_region

CONFIG = fedmsg.config.load_config()
fedmsg.meta.make_processors(**CONFIG)

_cache = make_region(
    key_mangler=lambda key: "fmn.consumer:dogpile:" + key
).configure(**CONFIG['fmn.rules.cache'].copy())

log = logging.getLogger("moksha.hub")

default_url = 'https://admin.fedoraproject.org/accounts/'
creds = CONFIG['fas_credentials']

fasclient = fedora.client.fas2.AccountSystem(
    base_url=creds.get('base_url', default_url),
    username=creds['username'],
    password=creds['password'],
)


def make_fas_cache(**config):
    log.warn("Building the FAS cache into redis.")
    if _cache.get('fas_cache_built'):
        log.warn("FAS cache already built into redis.")
        return

    global fasclient
    timeout = socket.getdefaulttimeout()
    for key in string.ascii_lowercase:
        socket.setdefaulttimeout(600)
        try:
            log.info("Downloading FAS cache for %s*" % key)
            print(key)
            request = fasclient.send_request(
                '/user/list',
                req_params={
                    'search': '%s*' % key,
                    'status': 'active'
                },
                auth=True)
        except fedora.client.ServerError as e:
            log.warning("Failed to download fas cache for %s %r" % (key, e))
            return {}
        finally:
            socket.setdefaulttimeout(timeout)

        log.info("Caching necessary user data")
        for user in request['people']:
            nick = user['ircnick']
            if nick:
                _cache.set(str(nick), user['username'])

            email = user['email']
            if email:
                _cache.set(str(email), user['username'])

        del request

    _cache.set('fas_cache_built', True)


def update_nick(username):
    global fasclient
    try:
        log.info("Downloading FAS cache for %s*" % username)
        request = fasclient.send_request(
            '/user/list',
            req_params={'search': '%s' % username},
            auth=True)
    except fedora.client.ServerError as e:
        log.warning(
            "Failed to download fas cache for %s: %r" % (username, e))
        return {}

    log.info("Caching necessary data for %s" % username)
    for user in request['people']:
        nick = user['ircnick']
        if nick:
            _cache.set(nick, user['username'])

        email = user['email']
        if email:
            _cache.set(email, user['username'])
    else:
        # If we couldn't find the nick in FAS, save it in the _cache as nick
        # so that we avoid calling FAS for every single filter we have to
        # run through
        _cache.set(username, username)


def update_email(email):
    global fasclient
    try:
        log.info("Downloading FAS cache for %s" % email)
        request = fasclient.send_request(
            '/user/list',
            req_params={
                'search': '%s' % email,
                'by_email': 1,
            },
            auth=True)
    except fedora.client.ServerError as e:
        log.warning(
            "Failed to download fas cache for %s: %r" % (email, e))
        return {}

    log.info("Caching necessary data for %s" % email)
    for user in request['people']:
        nick = user['ircnick']
        if nick:
            _cache.set(nick, user['username'])

        email = user['email']
        if email:
            _cache.set(email, user['username'])
    else:
        # If we couldn't find the email in FAS, save it in the _cache as
        # email so that we avoid calling FAS for every single filter we
        # have to run through
        _cache.set(email, email)


def nick2fas(nickname, **config):
    result = _cache.get(nickname)
    if not result:
        update_nick(nickname)
        result = _cache.get(nickname)
    return result or nickname


def email2fas(email, **config):
    if email.endswith('@fedoraproject.org'):
        return email.rsplit('@', 1)[0]

    result = _cache.get(email)
    if not result:
        update_email(email)
        result = _cache.get(email)
    return result or email
