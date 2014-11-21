

def bugzilla_bug_new(config, message):
    """ Bugzilla: a user filed a new bug

    Adding this rule will trigger notifications when a user **files** a new bug in
    `Bugzilla <https://bugzilla.redhat.com>`_ for **Fedora** or **Fedora EPEL** products.
    """
    return message['topic'].endswith('bugzilla.bug.new')


def bugzilla_bug_update(config, message):
    """ Bugzilla: a user updated a bug

    Adding this rule will trigger notifications when a user **updates** a bug in
    `Bugzilla <https://bugzilla.redhat.com>`_ for **Fedora** or **Fedora EPEL** products.
    """
    return message['topic'].endswith('bugzilla.bug.update')


