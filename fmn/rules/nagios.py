from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['nagios'])
def nagios_catchall(config, message, **kwargs):
    """ Nagios notifications

    This rule lets through messages from Fedora Infrastructure's `nagios
    instance <https://admin.fedoraproject.org/nagios>`_ about service health.
    """
    return message['topic'].split('.')[3] == 'nagios'
