""" Fedora Notifications pkgdb client """

import logging
import time

import requests
import requests.exceptions

import fedmsg.meta

from dogpile.cache import make_region
from fedora.client.fas2 import AccountSystem

log = logging.getLogger(__name__)

try:
    import re2 as re
except ImportError:
    log.warning("Couldn't import the 're2' module.")
    import re

# We cache fancy stuff here from pkgdb, etc.. stuff that we want to expire.
_cache = make_region()
_FAS = None

# This doesn't need any expiration.  Cache forever.
# We do this because the compilation step for python-re2 is 16x slower than
# stdlib, but the match is 10x faster.  So, cache the slow part once and use
# the fast part at the tightest part of the loop.
_regex_cache = {}


def compile_regex(pattern):
    if not pattern in _regex_cache:
        # This is expensive with python-re2, so we cache it.  Forever.
        _regex_cache[pattern] = re.compile(pattern)
    return _regex_cache[pattern]


def get_fas(config):
    """ Return a fedora.client.fas2.AccountSystem object if the provided
    configuration contains a FAS username and password.
    """
    global _FAS
    if _FAS is not None:
        return _FAS

    # In some development environments, having fas_credentials around is a
    # pain.. so, let things proceed here, but emit a warning.
    try:
        creds = config['fas_credentials']
    except KeyError:
        log.warn("No fas_credentials available.  Unable to query FAS.")
        return None

    default_url = 'https://admin.fedoraproject.org/accounts/'

    _FAS = AccountSystem(
        creds.get('base_url', default_url),
        username=creds['username'],
        password=creds['password'],
        cache_session=False,
        insecure=creds.get('insecure', False)
    )

    return _FAS


def get_packagers_of_package(config, package):
    """ Retrieve the list of users who have commit on a package.

    :arg config: a dict containing the fedmsg config
    :arg package: the package you are interested in.
    :return: a set listing all the fas usernames that have some ACL on package.
    """

    if not _cache.is_configured:
        _cache.configure(**config['fmn.rules.cache'])

    key = cache_key_generator(get_packagers_of_package, package)
    creator = lambda: _get_pkgdb2_packagers_for(config, package)
    return _cache.get_or_create(key, creator)


def _get_pkgdb2_packagers_for(config, package):
    log.debug("Requesting pkgdb2 packagers of package %r" % package)

    default = 'https://admin.fedoraproject.org/pkgdb/api'
    base = config.get('fmn.rules.utils.pkgdb_url', default)
    url = '{0}/package/{1}'.format(base, package)
    log.info("hitting url: %r" % url)
    req = requests.get(url)

    if not req.status_code == 200:
        log.debug('URL %s returned code %s', req.url, req.status_code)
        return set()

    data = req.json()

    if not data['packages'] or not 'acls' in data['packages'][0]:
        return set()

    obj = data['packages'][0]

    packagers = set([
        acl['fas_name'] for acl in obj['acls']
        if acl['status'] == 'Approved'])

    groups = set([
        acl['fas_name'].replace('group::', '')
        for acl in obj['acls'] if (
            acl['status'] == 'Approved' and
            acl['fas_name'].startswith('group::'))
    ])
    if groups:
        fas = get_fas(config)
    for group in groups:
        packagers.update(get_user_of_group(config, fas, group))

    return packagers


def get_packages_of_user(config, username, flags):
    """ Retrieve the list of packages where the specified user some acl.

    :arg config: a dict containing the fedmsg config
    :arg username: the fas username of the packager whose packages are of
        interest.
    :return: a set listing all the packages where the specified user has
        some ACL.

    """

    if not _cache.is_configured:
        _cache.configure(**config['fmn.rules.cache'])

    packages = []

    groups = get_groups_of_user(config, get_fas(config), username)
    owners = [username] + ['group::' + group for group in groups]

    for owner in owners:
        key = cache_key_generator(get_packages_of_user, owner)
        creator = lambda: _get_pkgdb2_packages_for(config, owner, flags)
        subset = _cache.get_or_create(key, creator)
        packages.extend(subset)

    return set(packages)


def cache_key_generator(fn, arg):
    return "|".join([fn.__module__, fn.__name__, arg]).encode('utf-8')


def invalidate_cache_for(config, fn, arg):
    if not _cache.is_configured:
        _cache.configure(**config['fmn.rules.cache'])

    key = cache_key_generator(fn, arg)
    return _cache.delete(key)


def _get_pkgdb2_packages_for(config, username, flags):
    log.debug("Requesting pkgdb2 packages for user %r" % username)
    start = time.time()

    default = 'https://admin.fedoraproject.org/pkgdb/api'
    base = config.get('fmn.rules.utils.pkgdb_url', default)

    url = '{0}/packager/package/{1}'.format(base, username)
    log.info("hitting url: %r" % url)
    req = requests.get(url)

    if not req.status_code == 200:
        log.debug('URL %s returned code %s', req.url, req.status_code)
        return set()

    data = req.json()

    packages_of_interest = sum([data[flag] for flag in flags], [])
    packages_of_interest = set([p['name'] for p in packages_of_interest])
    log.debug("done talking with pkgdb2 for now.  %0.2fs", time.time() - start)
    return packages_of_interest


def get_user_of_group(config, fas, groupname):
    ''' Return the list of users in the specified group.

    :arg config: a dict containing the fedmsg config
    :arg fas: a fedora.client.fas2.AccountSystem object instanciated and loged
        into FAS.
    :arg groupname: the name of the group for which we want to retrieve the
        members.
    :return: a list of FAS user members of the specified group.
    '''

    if not _cache.is_configured:
        _cache.configure(**config['fmn.rules.cache'])

    key = cache_key_generator(get_user_of_group, groupname)
    def creator():
        if not fas:
            return set()
        return set([u.username for u in fas.group_members(groupname)])
    return _cache.get_or_create(key, creator)


def get_groups_of_user(config, fas, username):
    ''' Return the list of (pkgdb) groups to which the user belongs.

    :arg config: a dict containing the fedmsg config
    :arg fas: a fedora.client.fas2.AccountSystem object instanciated and loged
        into FAS.
    :arg username: the name of a user for which we want to retrieve groups
    :return: a list of FAS groups to which the user belongs.
    '''

    if not _cache.is_configured:
        _cache.configure(**config['fmn.rules.cache'])

    key = cache_key_generator(get_groups_of_user, username)

    def creator():
        if not fas:
            return []
        results = []
        for group in fas.person_by_username(username).get('memberships', []):
            if group['group_type'] == 'pkgdb':
                results.append(group.name)
        return results

    return _cache.get_or_create(key, creator)


def msg2usernames(msg, **config):
    ''' Return cached fedmsg.meta.msg2usernames(...) '''

    if not _cache.is_configured:
        _cache.configure(**config['fmn.rules.cache'])

    key = "|".join(['usernames', msg['msg_id']]).encode('utf-8')
    creator = lambda: fedmsg.meta.msg2usernames(msg, **config)
    return _cache.get_or_create(key, creator)


def msg2packages(msg, **config):
    ''' Return cached fedmsg.meta.msg2packages(...) '''

    if not _cache.is_configured:
        _cache.configure(**config['fmn.rules.cache'])

    key = "|".join(['packages', msg['msg_id']]).encode('utf-8')
    creator = lambda: fedmsg.meta.msg2packages(msg, **config)
    return _cache.get_or_create(key, creator)
