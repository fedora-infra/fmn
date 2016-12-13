from fmn.lib.hinting import hint


@hint(categories=['infragit'])
def all_infragit(config, message):
    """ Git commits to fedora-infra repos

    The `Fedora Infrastructure team
    <https://fedoraproject.org/wiki/Infrastructure>`_ maintains `a handful of
    git repos <https://infrastructure.fedoraproject.org/cgit/>`_ for the
    configuration of its environments.

    This rule will let through messages *all* git messages from fedora-infra
    repos.
    """
    return '.infragit.' in message['topic']
