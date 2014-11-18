def pkgdb_acl_update(config, message):
    """ Pkgdb: a user updated an ACL

    Adding this rule will trigger notifications when an ACL on a package
    is **updated** in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.acl.update')


def pkgdb_acl_delete(config, message):
    """ Pkgdb: a user deleted an ACL

    Adding this rule will trigger notifications when an ACL on a package
    is **deleted** in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.acl.delete')


def pkgdb_admin_action_status_update(config, message):
    """ Pkgdb: an admin updated the status of Admin Action.

    Adding this rule will trigger notifications when an admin **updates**
    the status of Admin Action in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.admin.action.status.update')


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


def pkgdb_owner_update(config, message):
    """ Pkgdb: a user updated the owner of a package

    Adding this rule will trigger notifications when the **owner** of a package
    in the Fedora `Package DB <https://admin.fedoraproject.org/pkgdb>`_
    **changes**.  This includes when a package is orphaned.
    """
    return message['topic'].endswith('pkgdb.owner.update')


def pkgdb_package_branch_delete(config, message):
    """ Pkgdb: an admin deleted a branch of a package

    Adding this rule will trigger notifications when an admin **deletes**
    a branch of a package in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.package.branch.delete')


def pkgdb_package_branch_new(config, message):
    """ Pkgdb: a new branch is created for a package

    Adding this rule will trigger notifications when a **new branch** is
    **created** for a package in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.package.branch.new')


def pkgdb_package_branch_request(config, message):
    """ Pkgdb: a user requested a new branch for a package

    Adding this rule will trigger notifications when a user **requests** a
    **new branch** for a package in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.package.branch.request')


def pkgdb_package_new(config, message):
    """ Pkgdb: a new package has been created

    Adding this rule will trigger notifications when a **new package is
    created** in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.  This typically happens near the
    end of the Package Review Process as a result of a `SCM Admin Request
    <http://fedoraproject.org/wiki/Package_SCM_admin_requests>`_.
    """
    return message['topic'].endswith('pkgdb.package.new')


def pkgdb_package_critpath_update(config, message):
    """ Pkgdb: an admin updated the critpath flag

    Adding this rule will trigger notifications when **the critical path
    flag** of a package in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_ **updates**.
    """
    return message['topic'].endswith('pkgdb.package.critpath.update')


def pkgdb_package_delete(config, message):
    """ Pkgdb: an admin deleted a package

    Adding this rule will trigger notifications when an admin **deletes** a
    package in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.package.delete')


def pkgdb_package_monitor_update(config, message):
    """ Pkgdb: an admin updated monitoring status

    Adding this rule will trigger notifications when an admin **updates**
    **monitoring status** for a package in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.package.montior.update')


def pkgdb_package_new_request(config, message):
    """ Pkgdb: a user requested a new package

    Adding this rule will trigger notifications when a user **requests** a
    **new package** to be added in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.package.new.request')


def pkgdb_package_update(config, message):
    """ Pkgdb: a user updated information about a package

    Adding this rule will trigger notifications when a **package's details are
    updated** in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.package.update')


def pkgdb_package_update_status(config, message):
    """ Pkgdb: a user updated the status of a package

    Adding this rule will trigger notifications when a **package's status is
    updated** in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.package.update.status')
