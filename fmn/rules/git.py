from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['git'])
def git_catchall(config, message):
    """ All dist-git activity

    Adding this rule will indiscriminately match notifications of all types
    from `dist-git <http://pkgs.fedoraproject.org/cgit>`_.
    """
    return message['topic'].split('.')[3] == 'git'


@hint(topics=[_('git.branch')])
def git_branch(config, message):
    """ New dist-git branches for packages

    Include this rule to receive notifications of new branches being created
    for Fedora package git repos.
    """
    return message['topic'] == _('git.branch')


@hint(topics=[_('git.lookaside.new')])
def git_lookaside_new(config, message):
    """ New tarballs uploaded to the lookaside cache

    Include this rule to receive notifications of new sources being uploaded
    to the "lookaside cache" as when someone runs ``fedpkg new-sources
    <TARBALL>``.
    """
    return message['topic'].endswith('git.lookaside.new')


@hint(topics=[_('git.mass_branch.complete')])
def git_mass_branch_complete(config, message):
    """ Mass-branch completes

    There is a script called ``pkgdb2branch`` that gets run by an SCM
    admin, typically as part of the new package process.

    This rule will include messages from when that script **finishes** a "mass
    branch".
    """
    return message['topic'].endswith('git.mass_branch.complete')


@hint(topics=[_('git.mass_branch.start')])
def git_mass_branch_start(config, message):
    """ Mass-branch begins

    There is a script called ``pkgdb2branch`` that gets run by an SCM
    admin, typically as part of the new package process.

    This rule will include messages from when that script is instructed to
    carry out a "mass branch" of all packages.
    """
    return message['topic'].endswith('git.mass_branch.start')


@hint(topics=[_('git.pkgdb2branch.complete')])
def git_pkgdb2branch_complete(config, message):
    """ pkgdb2branch completes

    There is a script called ``pkgdb2branch`` that gets run by an SCM
    admin as part of the new package process.  Typically, when an `SCM Admin
    Request <http://fedoraproject.org/wiki/Package_SCM_admin_requests>`_ is
    approved, the scm admin will add the new package or branch to the package
    database.  *After that*, the scm admin will run ``pkgdb2branch`` to create
    the branch in git on the file system.

    This rule will include messages from when that process **completes**.
    """
    return message['topic'].endswith('git.pkgdb2branch.complete')



@hint(topics=[_('git.pkgdb2branch.start')])
def git_pkgdb2branch_start(config, message):
    """ pkgdb2branch starts

    There is a script called ``pkgdb2branch`` that gets run by an SCM
    admin as part of the new package process.  Typically, when an `SCM Admin
    Request <http://fedoraproject.org/wiki/Package_SCM_admin_requests>`_ is
    approved, the scm admin will add the new package or branch to the package
    database.  *After that*, the scm admin will run ``pkgdb2branch`` to create
    the branch in git on the file system.

    This rule will include messages from when that process **begins**.
    """
    return message['topic'].endswith('git.pkgdb2branch.start')


@hint(topics=[_('git.receive')])
def git_receive(config, message):
    """ Git pushes to dist-git

    Including this rule will produce notifications triggered when somebody runs
    ``fedpkg push`` on a package.
    """
    return message['topic'] == _('git.receive')
