""" Fedora Notifications pkgdb client """

import json
import logging
import requests
import requests.exceptions

from dogpile.cache import make_region

log = logging.getLogger(__name__)

_cache = make_region()


def get_packagers_of_package(config, package):
    """ Retrieve the list of users who have commit on a package.

    :arg config: a dict containing the fedmsg config
    :arg package: the package you are interested in.
    :return: a set listing all the fas usernames that have some ACL on package.
    """

    if not hasattr(_cache, 'backend'):
        _cache.configure(**config['fmn.rules.cache'])

    @_cache.cache_on_arguments()
    def _getter(package):
        """ Cached access to pkgdb2 """
        def _get(attempt=0):
            """ Try at most three times before giving up if err """
            try:
                return _get_pkgdb2_packagers_for(config, package)
            except requests.exceptions.ConnectionError:
                if attempt >= 3:
                    raise
                return _get(attempt + 1)
        return _get()

    return _getter(package)


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

    @_cache.cache_on_arguments()
    def _getter(username):
        return _get_pkgdb2_packages_for(config, username)

    return _getter(username)


def _get_pkgdb2_packages_for(config, username):
    log.debug("Requesting pkgdb2 packages for user %r" % username)

    def _get_page(page):
        url = '{0}/packager/acl/{1}'.format(
                    config['fmn.rules.utils.pkgdb_url'], username)
        log.info("hitting url: %r" % url)
        req = requests.get(url, params=dict(page=page))

        if not req.status_code == 200:
            log.debug('URL %s returned code %s', req.url, req.status_code)
            return None

        return req.json()

    # We have to request the first page of data to figure out the total number
    packages = set()
    data = _get_page(1)

    if data is None:
        return packages

    pages = data['page_total']

    for i in range(1, pages + 1):

        # Avoid requesting the data twice the first time around
        if i != 1:
            data = _get_page(i)

        if data is None:
            continue

        for pkgacl in data['acls']:
            if pkgacl['status'] != 'Approved':
                continue

            packages.add(pkgacl['packagelist']['package']['name'])

    log.debug("done talking with pkgdb2 for now.")
    return packages
