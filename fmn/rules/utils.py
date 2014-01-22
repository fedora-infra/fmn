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
        if config.get('fmn.rules.utils.use_pkgdb2', True):
            return _get_pkgdb2_packages_for(config, username)
        else:
            return _get_pkgdb1_packages_for(config, username)

    return _getter(username)


def _get_pkgdb2_packages_for(config, username):
    log.debug("Requesting pkgdb2 packages for user %r" % username)
    req = requests.get('{0}/packager/acl/{1}'.format(
        fmn.config['fmn.rules.utils.pkgdb2_api_url'], username))
    if not req.status_code == 200:
        return []
    data = json.loads(req.text)
    packages = set()
    for pkgacl in data['acls']:
        if pkgacl['status'] != 'Approved':
            continue
        packages.add(pkgacl['packagelist']['package']['name'])
    log.debug("done talking with pkgdb2 for now.")
    return packages


# TODO -- delete this once pkgdb2 goes live.
def _get_pkgdb1_packages_for(config, username):
    log.debug("Requesting pkgdb1 packages for user %r" % username)
    pkgdb1_base_url = 'https://admin.fedoraproject.org/pkgdb'
    req = requests.get('{0}/users/packages/{1}?tg_format=json'.format(
        pkgdb1_base_url, username))
    if not req.status_code == 200:
        return []
    data = json.loads(req.text)
    packages = set([pkg['name'] for pkg in data['pkgs']])
    log.debug("done talking with pkgdb1 for now.")
    return packages
