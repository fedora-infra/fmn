""" Fedora Notifications pkgdb client """

import json
import logging
import requests
import requests.exceptions

from dogpile.cache import make_region
from fedora.client.fas2 import AccountSystem

log = logging.getLogger(__name__)

_cache = make_region()
_FAS = None


def get_fas(config):
    """ Return a fedora.client.fas2.AccountSystem object if the provided
    configuration contains a FAS username and password.
    """
    global _FAS
    if _FAS is not None:
        return _FAS

    creds = config['fas_credentials']
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

    if not hasattr(_cache, 'backend'):
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
        for acl in obj['acls']
        if acl['status'] == 'Approved' and acl['fas_name'].startswith('group::')
    ])
    if groups:
        fas = get_fas(config)
    for group in groups:
        packagers.update(get_user_of_group(config, fas, group))

    return packagers


def get_packages_of_user(config, username):
    """ Retrieve the list of packages where the specified user some acl.

    :arg config: a dict containing the fedmsg config
    :arg username: the fas username of the packager whose packages are of
        interest.
    :return: a set listing all the packages where the specified user has
        some ACL.

    """

    if not hasattr(_cache, 'backend'):
        _cache.configure(**config['fmn.rules.cache'])

    key = cache_key_generator(get_packages_of_user, username)
    creator = lambda: _get_pkgdb2_packages_for(config, username)
    return _cache.get_or_create(key, creator)


def cache_key_generator(fn, arg):
    return "|".join([fn.__module__, fn.__name__, arg]).encode('utf-8')


def invalidate_cache_for(config, fn, arg):
    if not hasattr(_cache, 'backend'):
        _cache.configure(**config['fmn.rules.cache'])

    key = cache_key_generator(fn, arg)
    return _cache.delete(key)


def _get_pkgdb2_packages_for(config, username):
    log.debug("Requesting pkgdb2 packages for user %r" % username)

    default = 'https://admin.fedoraproject.org/pkgdb/api'
    base = config.get('fmn.rules.utils.pkgdb_url', default)

    url = '{0}/packager/package/{1}'.format(base, username)
    log.info("hitting url: %r" % url)
    req = requests.get(url)

    if not req.status_code == 200:
        log.debug('URL %s returned code %s', req.url, req.status_code)
        return set()

    data = req.json()

    packages_of_interest = data['point of contact'] + data['co-maintained']
    packages_of_interest = set([p['name'] for p in packages_of_interest])
    log.debug("done talking with pkgdb2 for now.")
    return packages_of_interest


def get_user_of_group(config, fas, groupname):
    ''' Return the list of user in the specified group.
    
    :arg config: a dict containing the fedmsg config
    :arg fas: a fedora.client.fas2.AccountSystem object instanciated and loged
        into FAS.
    :arg groupname: the name of the group for which we want to retrieve the
        members.
    :return: a list of FAS user members of the specified group.
    '''

    if not hasattr(_cache, 'backend'):
        cache.configure(**config['fmn.rules.cache'])

    key = cache_key_generator(get_user_of_group, groupname)
    creator = lambda: fas.group_members(groupname)
    return _cache.get_or_create(key, creator)

