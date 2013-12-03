def git_branch(config, message):
    """ Git: A new branch has been created in the git of package

    Include this rule to receive notifications of new branches being created
    for Fedora package git repos.
    """
    return message['topic'].endswith('git.branch')


def git_lookaside_new(config, message):
    """ Git: New sources have been uploaded to the "lookaside cache"

    Include this rule to receive notifications of of new sources being uploaded
    to the "lookaside cache" as when someone runs ``fedpkg new-sources
    <TARBALL>``.
    """
    return message['topic'].endswith('git.lookaside.new')


def git_mass_branch_complete(config, message):
    """ Git: Mass branching process completed

    There is a script called ``pkgdb2branch`` that gets run by an SCM
    admin, typically as part of the new package process.

    This rule will include messages from when that script **finishes** a "mass
    branch".
    """
    return message['topic'].endswith('git.mass_branch.complete')


def git_mass_branch_start(config, message):
    """Git: Mass branching process started

    There is a script called ``pkgdb2branch`` that gets run by an SCM
    admin, typically as part of the new package process.

    This rule will include messages from when that script is instructed to
    carry out a "mass branch" of all packages.
    """
    return message['topic'].endswith('git.mass_branch.start')


def git_pkgdb2branch_complete(config, message):
    """Git: Process to set branches on a package completed

    There is a script called ``pkgdb2branch`` that gets run by an SCM
    admin as part of the new package process.  Typically, when an `SCM Admin
    Request <http://fedoraproject.org/wiki/Package_SCM_admin_requests>`_ is
    approved, the scm admin will add the new package or branch to the package
    database.  *After that*, the scm admin will run ``pkgdb2branch`` to create
    the branch in git on the file system.

    This rule will include messages from when that process **completes**.
    """
    return message['topic'].endswith('git.pkgdb2branch.complete')



def git_pkgdb2branch_start(config, message):
    """Git: Process to set branches on a package started

    There is a script called ``pkgdb2branch`` that gets run by an SCM
    admin as part of the new package process.  Typically, when an `SCM Admin
    Request <http://fedoraproject.org/wiki/Package_SCM_admin_requests>`_ is
    approved, the scm admin will add the new package or branch to the package
    database.  *After that*, the scm admin will run ``pkgdb2branch`` to create
    the branch in git on the file system.

    This rule will include messages from when that process **begins**.
    """
    return message['topic'].endswith('git.pkgdb2branch.start')


def git_receive(config, message):
    """ Git: Changes have been pushed onto the git of a package

    Including this rule will produce notifications triggered when somebody runs
    ``fedpkg push`` on a package.
    """
    return message['topic'].endswith('git.receive')
