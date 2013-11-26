def pkgdb_acl_update(config, message):
    """ Pkgdb: a user updated an ACL

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('pkgdb.acl.update')


def pkgdb_acl_user_remove(config, message):
    """ Pkgdb: a user removed an ACL

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('pkgdb.acl.user.remove')


def pkgdb_branch_clone(config, message):
    """ Pkgdb: branched a specific package

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('pkgdb.branch.clone')


def pkgdb_branch_complete(config, message):
    """ Pkgdb: finished the branching process

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('pkgdb.branch.complete')


def pkgdb_branch_start(config, message):
    """ Pkgdb: started the branching process

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('pkgdb.branch.start')


def pkgdb_collection_new(config, message):
    """ Pkgdb: new collection created

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('pkgdb.collection.new')


def pkgdb_collection_update(config, message):
    """ Pkgdb: a collection has been updated

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('pkgdb.collection.update')


def pkgdb_critpath_update(config, message):
    """ Pkgdb: a user updated a critpath status

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('pkgdb.critpath.update')


def pkgdb_owner_update(config, message):
    """ Pkgdb: a user updated the owner of a package

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('pkgdb.owner.update')


def pkgdb_package_new(config, message):
    """ Pkgdb: a new package has been created

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('pkgdb.package.new')


def pkgdb_package_retire(config, message):
    """ Pkgdb: a package has been retired

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('pkgdb.package.retire')


def pkgdb_package_update(config, message):
    """ Pkgdb: a user updated information about a package

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('pkgdb.package.update')
