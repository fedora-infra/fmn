""" Fedora Notifications pkgdb client """

import json
import logging
import requests
log = logging.getLogger(__name__)


## TODO: cache the results of this method
# This might mean removing the acl and branch argument
# Can be done using dogpile.cache
def get_packages_of_user(config, username, acl='commit', branch=None):
    """ Retrieve the list of packages where the specified user has the
    specified acl on the specified branch.

    :arg config: a dict containing the fedmsg config
    :arg username: the fas username of the packager whose packages are of
        interest.
    :kwarg acl: the acl that the specified user has on the packages
        returned. Defaults to ``commit``.
    :kwarg branch: the branch on which the specified user has the specified
        acl. Defaults to ``None`` == all branches.
    :return: a set listing all the packages where the specified user has
        the specified ACL on the specified branch(es).

    """

    if config.get('fmn.rules.utils.use_pkgdb2', True):
        return _get_pkgdb2_packages_for(config, username, acl, branch)
    else:
        return _get_pkgdb1_packages_for(config, username, acl, branch)


def _get_pkgdb2_packages_for(config, username, acl, branch):
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
        if pkgacl['acl'] != acl:
            continue
        if branch and pkgacl['packagelist']['collection']['branchname'] != branch:
            continue
        packages.add(pkgacl['packagelist']['package']['name'])
    log.debug("done talking with pkgdb2 for now.")
    return packages


# TODO -- delete this once pkgdb2 goes live.
def _get_pkgdb1_packages_for(config, username, acl, branch):
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
