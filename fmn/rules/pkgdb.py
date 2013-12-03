def pkgdb_acl_update(config, message):
    """ Pkgdb: a user updated an ACL

    Adding this rule will trigger notifications when an ACL on a package
    is **updated** in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.acl.update')


def pkgdb_acl_user_remove(config, message):
    """ Pkgdb: a user removed an ACL

    Adding this rule will trigger notifications when an ACL on a package
    is **removed** from the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.acl.user.remove')


def pkgdb_branch_clone(config, message):
    """ Pkgdb: branched a specific package

    Adding this rule will trigger notifications when a new branch is cloned
    for a package in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.branch.clone')


def pkgdb_branch_complete(config, message):
    """ Pkgdb: finished the branching process

    Adding this rule will trigger notifications when the **branching process
    completes** for a package in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.branch.complete')


def pkgdb_branch_start(config, message):
    """ Pkgdb: started the branching process

    Adding this rule will trigger notifications when the **branching process
    starts** for a package in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.branch.start')


def pkgdb_collection_new(config, message):
    """ Pkgdb: new collection created

    Adding this rule will trigger notifications when an admin **creates
    a new collection** in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.collection.new')


def pkgdb_collection_update(config, message):
    """ Pkgdb: a collection has been updated

    Adding this rule will trigger notifications when an admin **updates
    a collection** in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.collection.update')


def pkgdb_critpath_update(config, message):
    """ Pkgdb: a user updated a critpath status

    Adding this rule will trigger notifications when **the critical path
    status** of a package in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_ **changes** (when a package is
    either added or removed from the critical path).
    """
    return message['topic'].endswith('pkgdb.critpath.update')


def pkgdb_owner_update(config, message):
    """ Pkgdb: a user updated the owner of a package

    Adding this rule will trigger notifications when the **owner** of a package
    in the Fedora `Package DB <https://admin.fedoraproject.org/pkgdb>`_
    **changes**.  This includes when a package is orphaned.
    """
    return message['topic'].endswith('pkgdb.owner.update')


def pkgdb_package_new(config, message):
    """ Pkgdb: a new package has been created

    Adding this rule will trigger notifications when a **new package is
    created** in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.  This typically happens near the
    end of the Package Review Process as a result of a `SCM Admin Request
    <http://fedoraproject.org/wiki/Package_SCM_admin_requests>`_.
    """
    return message['topic'].endswith('pkgdb.package.new')


def pkgdb_package_retire(config, message):
    """ Pkgdb: a package has been retired

    Adding this rule will trigger notifications when a **package is
    retired** from the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.package.retire')


def pkgdb_package_update(config, message):
    """ Pkgdb: a user updated information about a package

    Adding this rule will trigger notifications when a **package's details are
    updated** in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.package.update')
