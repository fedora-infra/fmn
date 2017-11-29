""" Fedora Notifications pkgdb client """

from collections import defaultdict
import logging
import time

from six.moves.urllib.parse import urlencode
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

requests_session = requests.Session()


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


def _paginate_pagure_data(url, params):
    """
    Paginate over a Pagure URL.

    Args:
        url (str): The URL to paginate over, without any parameters.
        params (dict): A dictionary of URL parameters to use when querying Pagure.

    Yields:
        dict: The deserialized JSON response for a given page.
    """

    # Set up the first page query
    params['page'] = 1
    next_page_url = url + "?" + urlencode(params)

    while next_page_url:
        try:
            response = requests_session.get(next_page_url, timeout=25)
            if response.status_code == 200:
                data = response.json()
                # When we run out of pages, this will be None
                next_page_url = data['pagination']['next']
                yield data
            elif response.status_code == 404:
                # Pagure apparently returns 404 if the query returns an empty list?
                next_page_url = None
            else:
                log.error('Querying Pagure at %s returned code %s',
                          response.url, response.status_code)
                next_page_url = None

        except requests.exceptions.Timeout as e:
            log.warn('URL %s timed out %r', next_page_url, e)
            next_page_url = None


def get_packagers_of_package(config, package):
    """ Retrieve the list of users who have commit on a package.

    :arg config: a dict containing the fedmsg config
    :arg package: the package you are interested in.
    :return: a set listing all the fas usernames that have some ACL on package.
    """

    if not _cache.is_configured:
        _cache.configure(**config['fmn.rules.cache'].copy())

    key = cache_key_generator(get_packagers_of_package, package)
    creator = lambda: _get_packagers_for(config, package)
    return _cache.get_or_create(key, creator)


def _get_packagers_for(config, package):
    """ Get the packagers (users) associated with a given package.

    The list is gathered from either pkgdb2 (old) or pagure (new) depending on
    the configuration value of ``fmn.rules.utils.use_pagure_for_ownership``.

    Args:
        config (dict): The application configuration.
        package (str): The package name.
    Returns:
        set:  A `set` of packager usernames.
    """
    if config['fmn.rules.utils.use_pagure_for_ownership']:
        return _get_pagure_packagers_for(config, package)
    else:
        return _get_pkgdb2_packagers_for(config, package)


def _get_pagure_packagers_for(config, package):
    """ Get the packagers (users) associated with a given package in pagure.

    Args:
        config (dict): The application configuration.
        package (str): The package name.
    Returns:
        set:  A `set` of packager usernames.
    """
    base = config.get('fmn.rules.utils.pagure_api_url',
                      'https://src.fedoraproject.org/pagure/api')

    # Give a default namespace if one is not provided. See
    # https://github.com/fedora-infra/fmn/issues/208
    if '/' not in package:
        package = 'rpms/' + package

    url = '{0}/0/{1}'.format(base, package)
    log.info("Querying Pagure at %s for packager information", url)
    try:
        response = requests_session.get(url, params={'fork': False}, timeout=25)
    except requests.exceptions.Timeout as e:
        log.warn('URL %s timed out %r', url, e)
        return set()

    if response.status_code != 200:
        log.warn('URL %s returned code %s', response.url, response.status_code)
        return set()

    data = response.json()

    packagers = set(sum(data['access_users'].values(), []))
    groups = set(sum(data['access_groups'].values(), []))

    if groups:
        fas = get_fas(config)
    for group in groups:
        packagers.update(get_user_of_group(config, fas, group))

    return packagers


def _get_pkgdb2_packagers_for(config, package):
    """ Get the packagers (users) associated with a given package in pkgdb.

    Args:
        config (dict): The application configuration.
        package (str): The package name.
    Returns:
        set:  A `set` of packager usernames.
    """
    log.debug("Requesting pkgdb2 packagers of package %r" % package)

    base = config.get('fmn.rules.utils.pkgdb_url',
                      'https://admin.fedoraproject.org/pkgdb/api')
    url = '{0}/package/{1}'.format(base, package)
    log.info("Querying PkgDB at %s for packager information", url)
    try:
        req = requests_session.get(url, timeout=15)
    except requests.exceptions.Timeout as e:
        log.warn('URL %s timed out %r', url, e)
        return set()

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
        _cache.configure(**config['fmn.rules.cache'].copy())

    packages = defaultdict(set)

    groups = get_groups_of_user(config, get_fas(config), username)
    owners = [username] + ['group::' + group for group in groups]

    for owner in owners:
        key = cache_key_generator(get_packages_of_user, owner)
        creator = lambda: _get_packages_for(config, owner, flags)
        subset = _cache.get_or_create(key, creator)
        for namespace in subset:
            packages[namespace].update(subset[namespace])

    return dict(packages)


def cache_key_generator(fn, arg):
    return "|".join([fn.__module__, fn.__name__, arg]).encode('utf-8')


def invalidate_cache_for(config, fn, arg):
    if not _cache.is_configured:
        _cache.configure(**config['fmn.rules.cache'].copy())

    key = cache_key_generator(fn, arg)
    return _cache.delete(key)


def _get_packages_for(config, username, flags):
    """ Get the packages with which a user is associated.

    The list is gathered from either pkgdb2 (old) or pagure (new) depending on
    the configuration value of ``fmn.rules.utils.use_pagure_for_ownership``.

    Args:
        config (dict): The application configuration.
        username (str): The FAS username to fetch the packages for.
        flags (list): The type of relationship the user should have to the
            package (e.g. "watch", "point of contact", or "co-maintained").
    Returns:
        dict:  A `dict` mapping namespaces to sets of package names.
    """

    if config['fmn.rules.utils.use_pagure_for_ownership']:
        return _get_pagure_packages_for(config, username, flags)
    else:
        return _get_pkgdb2_packages_for(config, username, flags)


def _get_pkgdb2_packages_for(config, username, flags):
    """
    Get the packages a user is associated with from pkgdb2.

    Args:
        config (dict): The application configuration.
        username (str): The FAS username to fetch the packages for.
        flags (list): The type of relationship the user should have to the
            package (e.g. "watch", "point of contact", etc.). See the pkgdb2
            API for details.
    Returns:
        dict:  A `dict` mapping namespaces to sets of package names.
    """
    log.debug("Requesting pkgdb2 packages for user %r" % username)
    start = time.time()

    base = config.get('fmn.rules.utils.pkgdb_url',
                      'https://admin.fedoraproject.org/pkgdb/api')

    url = '{0}/packager/package/{1}'.format(base, username)
    log.info("Querying pkgdb at %s for packager information", url)

    try:
        req = requests_session.get(url, timeout=15)
    except requests.exceptions.Timeout as e:
        log.warn('URL %s timed out %r', url, e)
        return set()

    if not req.status_code == 200:
        log.debug('URL %s returned code %s', req.url, req.status_code)
        return {}

    data = req.json()

    packages = defaultdict(set)

    packages_of_interest = sum([data[flag] for flag in flags], [])
    for package in packages_of_interest:
        packages[package.get('namespace', 'rpms')].add(package['name'])
    log.debug("done talking with pkgdb2 for now.  %0.2fs", time.time() - start)
    return dict(packages)


def _get_pagure_packages_for(config, username, flags):
    """
    Get the packages a user is associated with from pagure.

    Args:
        config (dict): The application configuration.
        username (str): The FAS username to fetch the packages for.
        flags (list): The type of relationship the user should have to the
            package (e.g. "watch", "point of contact", etc.).

    Returns:
        dict:  A dictionary mapping namespaces to sets of package names.

    Raises:
        ValueError: If invalid flags are provided, or no flags are provided.
    """
    log.debug("Requesting pagure packages for user %r" % username)

    valid_flags = ['point of contact', 'co-maintained', 'watch']

    bogus = set(flags) - set(valid_flags)
    if bogus:
        raise ValueError(
            "{flags} are not valid owner flags for {user}.".format(flags=bogus, user=username))
    if len(flags) == 0:
        raise ValueError("No valid owner flags by which to query.")

    base = config.get('fmn.rules.utils.pagure_api_url',
                      'https://src.fedoraproject.org/api')
    url = base + '/0/projects'

    packages = defaultdict(set)
    for flag in flags:
        params = {'short': True, 'fork': False, 'per_page': 100}
        if flag == 'point of contact':
            params['owner'] = username
        elif flag == 'co-maintained':
            params['username'] = username
        else:  # watch
            # In the future we want to also support the 'watch' state.
            # See https://github.com/fedora-infra/fmn/issues/209
            # which depends on https://pagure.io/pagure/issue/2421
            log.debug('"watch" flag is currently unsupported, skipping')
            continue

        pages = _paginate_pagure_data(url, params)
        for page in pages:
            for repo in page['projects']:
                packages[repo['namespace']].add(repo['name'])

    return dict(packages)


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
        _cache.configure(**config['fmn.rules.cache'].copy())

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
        _cache.configure(**config['fmn.rules.cache'].copy())

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
        _cache.configure(**config['fmn.rules.cache'].copy())

    key = "|".join(['usernames', msg['msg_id']]).encode('utf-8')
    creator = lambda: fedmsg.meta.msg2usernames(msg, **config)
    return _cache.get_or_create(key, creator)


def msg2packages(msg, **config):
    ''' Return cached fedmsg.meta.msg2packages(...) '''

    if not _cache.is_configured:
        _cache.configure(**config['fmn.rules.cache'].copy())

    namespace = config.get('namespace', u'')
    key = u'|'.join([u'packages', namespace, msg['msg_id']]).encode('utf-8')
    creator = lambda: fedmsg.meta.msg2packages(msg, **config)
    return _cache.get_or_create(key, creator)
