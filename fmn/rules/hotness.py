from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('hotness.update.bug.file')])
def hotness_bug_file(config, message):
    """ New bugs filed for upstream releases

    There is a constellation of services involved in notifying packagers of
    `new upstream releases
    <https://fedoraproject.org/wiki/Upstream_release_monitoring>`_.
    Adding this rule will trigger notifications from the component called
    `the-new-hotness <https://github.com/fedora-infra/the-new-hotness>`_ when
    **a new RHBZ bug is opened** for a new upstream release of some package.
    """
    return message['topic'].endswith('hotness.update.bug.file')


@hint(topics=[_('hotness.update.bug.followup')])
def hotness_bug_followup(config, message):
    """ Automated koji activity on new upstream releases

    There is a constellation of services involved in notifying packagers of
    `new upstream releases
    <https://fedoraproject.org/wiki/Upstream_release_monitoring>`_.
    Adding this rule will trigger notifications from the component called
    `the-new-hotness <https://github.com/fedora-infra/the-new-hotness>`_ when
    it **follows up on an open ticket**.  This is sometimes to attempt an
    automated koji scratch build of a new upstream release, and other times to
    report that a real koji build by the owner of the package has succeeded.
    """
    return message['topic'].endswith('hotness.update.bug.followup')


@hint(topics=[_('hotness.update.drop')])
def hotness_update_drop(config, message):
    """ Failures to act on new upstream releases

    There is a constellation of services involved in notifying packagers of
    `new upstream releases
    <https://fedoraproject.org/wiki/Upstream_release_monitoring>`_.
    Adding this rule will trigger notifications from the component called
    `the-new-hotness <https://github.com/fedora-infra/the-new-hotness>`_ when
    it **fails to act on some new update** for some reason.  It might not know
    what the project is calledfooFedora, or it might be that connectivity with
    RHBZ failed. Sometimes the package owner just doesn't want RHBZ bugs
    filed.. and so they are dropped.
    """
    return message['topic'].endswith('hotness.update.drop')
