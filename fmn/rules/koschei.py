def koschei_package_state_change(config, message):
    """ Koschei: Package state has changed

    `Koschei <http://koschei.cloud.fedoraproject.org>`_ publishes this
    message when package's build or resolution state changes.
    """
    return message['topic'].endswith('koschei.package.state.change')

def koschei_group(config, message, group=None):
    """ Koschei: Messages pertaining to a package in given groups

    This rule limits message to particular
    `Koschei <http://koschei.cloud.fedoraproject.org>`_ groups. You can
    specify more groups separated by commas.
    """
    if not group or 'koschei' not in message['topic']:
        return False
    groups = set([item.strip() for item in group.split(',')])
    return bool(groups.intersection(message['msg'].get('groups')))
