from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('koschei.package.state.change')])
def koschei_package_state_change(config, message):
    """ Continuous integration state changes for a package (koschei)

    `Koschei <https://apps.fedoraproject.org/koschei/>`_ publishes
    this message when package's build or resolution state changes.
    """
    return message['topic'].endswith('koschei.package.state.change')


@hint(categories=['koschei'], invertible=False)
def koschei_group(config, message, group=None):
    """ Particular Koschei package groups

    This rule limits message to particular
    `Koschei <https://apps.fedoraproject.org/koschei/>`_ groups.
    You can specify more groups separated by commas.
    """
    if not group or 'koschei' not in message['topic']:
        return False
    groups = set([item.strip() for item in group.split(',')])
    return bool(groups.intersection(message['msg'].get('groups', [])))
