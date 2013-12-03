def compose_branched_complete(config, message):
    """ Release Engineering: Compose completed for a specific branch

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ completes
    the **entire** `compose <https://apps.fedoraproject.org/releng-dash/>`_ of
    the 'branched' Fedora pre-release.
    """
    return message['topic'].endswith('compose.branched.complete')


def compose_branched_mash_complete(config, message):
    """ Release Engineering: Mash completed for a specific branch

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ completes
    the **mash** phase of a `compose
    <https://apps.fedoraproject.org/releng-dash/>`_ of the 'branched' Fedora
    pre-release.
    """
    return message['topic'].endswith('compose.branched.mash.complete')


def compose_branched_mash_start(config, message):
    """ Release Engineering: Mash started for a specific branch

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ starts
    the **mash** phase of a `compose
    <https://apps.fedoraproject.org/releng-dash/>`_ of the 'branched' Fedora
    pre-release.
    """
    return message['topic'].endswith('compose.branched.mash.start')


def compose_branched_pungify_complete(config, message):
    """ Release Engineering: Pungi completed for a specific branch

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ completes
    the **pungi** phase of a `compose
    <https://apps.fedoraproject.org/releng-dash/>`_ of the 'branched' Fedora
    pre-release.
    """
    return message['topic'].endswith('compose.branched.pungify.complete')


def compose_branched_pungify_start(config, message):
    """ Release Engineering: Pungi started for a specific branch

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ starts
    the **pungi** phase of a `compose
    <https://apps.fedoraproject.org/releng-dash/>`_ of the 'branched' Fedora
    pre-release.
    """
    return message['topic'].endswith('compose.branched.pungify.start')


def compose_branched_rsync_complete(config, message):
    """ Release Engineering: rsync completed for a specific branch

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ finishes
    **rsyncing** a `compose <https://apps.fedoraproject.org/releng-dash/>`_ of
    the 'branched' Fedora pre-release.
    """
    return message['topic'].endswith('compose.branched.rsync.complete')


def compose_branched_rsync_start(config, message):
    """ Release Engineering: rsync started for a specific branch

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ starts
    **rsyncing** a `compose <https://apps.fedoraproject.org/releng-dash/>`_ of
    the 'branched' Fedora pre-release.
    """
    return message['topic'].endswith('compose.branched.rsync.start')


def compose_branched_start(config, message):
    """ Release Engineering: Compose started for a specific branch

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ starts
    the `compose <https://apps.fedoraproject.org/releng-dash/>`_ process for
    the 'branched' Fedora pre-release.
    """
    return message['topic'].endswith('compose.branched.start')

def compose_rawhide_complete(config, message):
    """ Release Engineering: Compose completed for rawhide

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ completes
    the **entire** `compose <https://apps.fedoraproject.org/releng-dash/>`_ of
    rawhide.
    """
    return message['topic'].endswith('compose.rawhide.complete')


def compose_rawhide_mash_complete(config, message):
    """ Release Engineering: Mash completed for rawhide

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ completes
    the **mash** phase of a `compose
    <https://apps.fedoraproject.org/releng-dash/>`_ of rawhide.
    """
    return message['topic'].endswith('compose.rawhide.mash.complete')


def compose_rawhide_mash_start(config, message):
    """ Release Engineering: Mash started for rawhide

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ starts
    the **mash** phase of a `compose
    <https://apps.fedoraproject.org/releng-dash/>`_ of rawhide.
    """
    return message['topic'].endswith('compose.rawhide.mash.start')


def compose_rawhide_pungify_complete(config, message):
    """ Release Engineering: Pungi completed for rawhide

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ completes
    the **pungi** phase of a `compose
    <https://apps.fedoraproject.org/releng-dash/>`_ of rawhide.
    """
    return message['topic'].endswith('compose.rawhide.pungify.complete')


def compose_rawhide_pungify_start(config, message):
    """ Release Engineering: Pungi started for rawhide

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ starts
    the **pungi** phase of a `compose
    <https://apps.fedoraproject.org/releng-dash/>`_ of rawhide.
    """
    return message['topic'].endswith('compose.rawhide.pungify.start')


def compose_rawhide_rsync_complete(config, message):
    """ Release Engineering: rsync completed for rawhide

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ finishes
    **rsyncing** a `compose <https://apps.fedoraproject.org/releng-dash/>`_ of
    rawhide.
    """
    return message['topic'].endswith('compose.rawhide.rsync.complete')


def compose_rawhide_rsync_start(config, message):
    """ Release Engineering: rsync started for rawhide

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ starts
    **rsyncing** a `compose <https://apps.fedoraproject.org/releng-dash/>`_ of
    rawhide.
    """
    return message['topic'].endswith('compose.rawhide.rsync.start')


def compose_rawhide_start(config, message):
    """ Release Engineering: Compose started for rawhide

    Adding this rule will allow through notifications published when `release
    engineering <https://fedoraproject.org/wiki/ReleaseEngineering>`_ starts
    the `compose <https://apps.fedoraproject.org/releng-dash/>`_ process for
    rawhide.
    """
    return message['topic'].endswith('compose.rawhide.start')
