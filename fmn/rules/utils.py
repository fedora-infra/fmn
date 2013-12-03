""" Fedora Notifications pkgdb client """

import json
import logging
import requests
log = logging.getLogger(__name__)

## TODO: Move this variable into a configuration file
PKGDB_API_URL = 'http://209.132.184.188/api/'


## TODO: cache the results of this method
# This might mean removing the acl and branch argument
# Can be done using dogpile.cache
def get_packages_of_user(username, acl='commit', branch=None):
    """ Retrieve the list of packages where the specified user has the
    specified acl on the specified branch.

    :arg username: the fas username of the packager whose packages are of
        interest.
    :kwarg acl: the acl that the specified user has on the packages
        returned. Defaults to ``commit``.
    :kwarg branch: the branch on which the specified user has the specified
        acl. Defaults to ``None`` == all branches.
    :return: a set listing all the packages where the specified user has
        the specified ACL on the specified branch(es).

    """
    req = requests.get(
        '{0}/packager/acl/{1}'.format(PKGDB_API_URL, username))
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
    return packages
