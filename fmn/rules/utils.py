""" Fedora Notifications pkgdb client """

import json
import logging
import requests

from dogpile.cache import make_region

log = logging.getLogger(__name__)

_cache = make_region()


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

        for pkgacl in data['acls']:
            if pkgacl['status'] != 'Approved':
                continue

            packages.add(pkgacl['packagelist']['package']['name'])

    log.debug("done talking with pkgdb2 for now.")
    return packages
