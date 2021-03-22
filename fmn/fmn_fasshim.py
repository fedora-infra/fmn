from __future__ import print_function

import logging
import socket
import string
import requests

import fedmsg
import fedmsg.meta
import fedora.client
import fedora.client.fas2
from dogpile.cache import make_region

from fmn import config
from .fasjson_client import Client

fedmsg.meta.make_processors(**config.app_conf)

_cache = make_region(
    key_mangler=lambda key: "fmn.consumer:dogpile:" + key
).configure(**config.app_conf['fmn.rules.cache'].copy())

log = logging.getLogger("moksha.hub")

default_url = 'https://admin.fedoraproject.org/accounts/'
creds = config.app_conf['fas_credentials']

fasjson = config.app_conf['fasjson']
if fasjson.get('active'):
    client = Client(url=fasjson.get('url', default_url))
else:
    client = fedora.client.fas2.AccountSystem(
        base_url=creds.get('base_url', default_url),
        username=creds['username'],
        password=creds['password'],
    )


def make_fasjson_cache(**config):
    log.warning("Building the FASJSON cache into redis.")
    if _cache.get('fas_cache_built'):
        log.warning("FASJSON cache already built into redis.")
        return
    global client
    try:
        _add_to_cache(list(client.list_all_entities("users")))
    except requests.exceptions.RequestException as e:
        log.error("Something went wrong building cache with error: %s" % e)
        return

    _cache.set('fas_cache_built', True)


def make_fas_cache(**config):
    log.warning("Building the FAS cache into redis.")
    if _cache.get('fas_cache_built'):
        log.warning("FAS cache already built into redis.")
        return

    global client
    timeout = socket.getdefaulttimeout()
    for key in string.ascii_lowercase:
        socket.setdefaulttimeout(600)
        try:
            log.info("Downloading FAS cache for %s*" % key)
            request = client.send_request(
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


def _add_to_cache(users):
    for user in users:
        nicks = user.get('ircnicks', [])
        for nick in nicks:
            _cache.set(nick, user['username'])

        emails = user.get('emails', [])
        for email in emails:
            _cache.set(email, user['username'])


def update_nick(username):
    global client
    if config.get('fasjson'):
        try:
            log.info("Downloading FASJSON cache for %s*" % username)
            response = client.get_user(username=username)
            _add_to_cache([response["result"]])
        except requests.exceptions.RequestException as e:
            log.error("Something went wrong updating the cache with error: %s" % e)
    else:
        try:
            log.info("Downloading FAS cache for %s*" % username)
            request = client.send_request(
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
    global client
    if config.get('fasjson'):
        try:
            log.info("Downloading FASJSON cache for %s*" % email)
            response = client.search(email=email)
            _add_to_cache(response['result'])
        except requests.exceptions.RequestException as e:
            log.error("Something went wrong updating the cache with error: %s" % e)
    else:
        try:
            log.info("Downloading FAS cache for %s" % email)
            request = client.send_request(
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
