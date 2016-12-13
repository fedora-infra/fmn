from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['pkgdb'])
def pkgdb_catchall(config, message):
    """ All Package DB events

    Adding this rule will indiscriminately match notifications of all types
    from `pkgdb2 <https://admin.fedoraproject.org/pkgdb>`_, i.e. ACL changes,
    new packages, requests for ownership, etc..
    """
    return message['topic'].split('.')[3] == 'pkgdb'


@hint(topics=[_('pkgdb.acl.update')])
def pkgdb_acl_update(config, message):
    """ Package ACL updates

    Adding this rule will trigger notifications when an ACL on a package
    is **updated** in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.acl.update')


@hint(topics=[_('pkgdb.acl.delete')])
def pkgdb_acl_delete(config, message):
    """ Package ACLs are deleted

    Adding this rule will trigger notifications when an ACL on a package
    is **deleted** in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.acl.delete')


@hint(topics=[_('pkgdb.admin.action.status.update')])
def pkgdb_admin_action_status_update(config, message):
    """ Pkgdb admin actions

    Adding this rule will trigger notifications when an admin **updates**
    the status of Admin Action in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.admin.action.status.update')


@hint(topics=[_('pkgdb.branch.complete')])
def pkgdb_branch_complete(config, message):
    """ Pkgdb branching process completes

    Adding this rule will trigger notifications when the **branching process
    completes** for a package in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.branch.complete')


@hint(topics=[_('pkgdb.branch.start')])
def pkgdb_branch_start(config, message):
    """ Pkgdb branching process starts

    Adding this rule will trigger notifications when the **branching process
    starts** for a package in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.branch.start')


@hint(topics=[_('pkgdb.collection.new')])
def pkgdb_collection_new(config, message):
    """ New pkgdb collections

    Adding this rule will trigger notifications when an admin **creates
    a new collection** in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.collection.new')


@hint(topics=[_('pkgdb.collection.update')])
def pkgdb_collection_update(config, message):
    """ Updates to pkgdb collections

    Adding this rule will trigger notifications when an admin **updates
    a collection** in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.collection.update')


@hint(topics=[_('pkgdb.owner.update')])
def pkgdb_owner_update(config, message):
    """ Package owner changes

    Adding this rule will trigger notifications when the **owner** of a package
    in the Fedora `Package DB <https://admin.fedoraproject.org/pkgdb>`_
    **changes**.  This includes when a package is orphaned.
    """
    return message['topic'].endswith('pkgdb.owner.update')


@hint(topics=[_('pkgdb.package.branch.delete')])
def pkgdb_package_branch_delete(config, message):
    """ Package branches are deleted

    Adding this rule will trigger notifications when an admin **deletes**
    a branch of a package in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.package.branch.delete')


@hint(topics=[_('pkgdb.package.branch.new')])
def pkgdb_package_branch_new(config, message):
    """ New package branches

    Adding this rule will trigger notifications when a **new branch** is
    **created** for a package in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.package.branch.new')


@hint(topics=[_('pkgdb.package.branch.request')])
def pkgdb_package_branch_request(config, message):
    """ Requests for new package branches

    Adding this rule will trigger notifications when a user **requests** a
    **new branch** for a package in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.package.branch.request')


@hint(topics=[_('pkgdb.package.new')])
def pkgdb_package_new(config, message):
    """ New packages

    Adding this rule will trigger notifications when a **new package is
    created** in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.  This typically happens near the
    end of the Package Review Process as a result of a `SCM Admin Request
    <http://fedoraproject.org/wiki/Package_SCM_admin_requests>`_.
    """
    return message['topic'].endswith('pkgdb.package.new')


@hint(topics=[_('pkgdb.package.critpath.update')])
def pkgdb_package_critpath_update(config, message):
    """ Critical path status changes

    Adding this rule will trigger notifications when **the critical path
    flag** of a package in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_ **updates**.
    """
    return message['topic'].endswith('pkgdb.package.critpath.update')


@hint(topics=[_('pkgdb.package.delete')])
def pkgdb_package_delete(config, message):
    """ Deleted packages

    Adding this rule will trigger notifications when an admin **deletes** a
    package in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.package.delete')


@hint(topics=[_('pkgdb.package.monitor.update')])
def pkgdb_package_monitor_update(config, message):
    """ Changes to the upstream-release-monitoring status of packages

    Adding this rule will trigger notifications when an admin **updates**
    **monitoring status** for a package in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.package.monitor.update')


@hint(topics=[_('pkgdb.package.new.request')])
def pkgdb_package_new_request(config, message):
    """ Requests for new packages

    Adding this rule will trigger notifications when a user **requests** a
    **new package** to be added in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.package.new.request')


@hint(topics=[_('pkgdb.package.update')])
def pkgdb_package_update(config, message):
    """ Changes to package details

    Adding this rule will trigger notifications when a **package's details are
    updated** in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.package.update')


@hint(topics=[_('pkgdb.package.update.status')])
def pkgdb_package_update_status(config, message):
    """ Package status changes

    Adding this rule will trigger notifications when a **package's status is
    updated** in the Fedora `Package DB
    <https://admin.fedoraproject.org/pkgdb>`_.
    """
    return message['topic'].endswith('pkgdb.package.update.status')
