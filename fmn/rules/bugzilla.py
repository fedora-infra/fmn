from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('bugzilla.bug.new')])
def bugzilla_bug_new(config, message):
    """ New RHBZ bugs

    Adding this rule will trigger notifications when a user **files** a new bug
    in `Bugzilla <https://bugzilla.redhat.com>`_ for **Fedora** or **Fedora
    EPEL** products.
    """
    return message['topic'].endswith('bugzilla.bug.new')


@hint(topics=[_('bugzilla.bug.update')])
def bugzilla_bug_update(config, message):
    """ Updates to existing RHBZ bugs

    Adding this rule will trigger notifications when a user **updates** a bug
    in `Bugzilla <https://bugzilla.redhat.com>`_ for **Fedora** or **Fedora
    EPEL** products.
    """
    return message['topic'].endswith('bugzilla.bug.update')
