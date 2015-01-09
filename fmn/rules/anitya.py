from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('anitya.distro.add', prefix='org.release-monitoring')])
def anitya_distro_add(config, message):
    """ Upstream: a distribution is added

    Adding this rule will trigger notifications when a new distribution is
    **added** to `anitya <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.distro.add')


@hint(topics=[_('anitya.distro.edit', prefix='org.release-monitoring')])
def anitya_distro_update(config, message):
    """ Upstream: a distribution has been updated

    Adding this rule will trigger notifications when a distribution is
    **updated** in `anitya <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.distro.edit')


@hint(topics=[_('anitya.project.add', prefix='org.release-monitoring')])
def anitya_project_add(config, message):
    """ Upstream: a project is added

    Adding this rule will trigger notifications when a project is **added**
    to `anitya <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.project.add')


@hint(topics=[_('anitya.project.add.tried', prefix='org.release-monitoring')])
def anitya_project_add_tried(config, message):
    """ Upstream: a project is tried to be added

    Adding this rule will trigger notifications when a project is tried to
    be **added** to `anitya <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.project.add.tried')


@hint(topics=[_('anitya.project.edit', prefix='org.release-monitoring')])
def anitya_project_update(config, message):
    """ Upstream: a project has been updated

    Adding this rule will trigger notifications when a project is **updated**
    in `anitya <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.project.edit')


@hint(topics=[_('anitya.project.map.new', prefix='org.release-monitoring')])
def anitya_mapping_new(config, message):
    """ Upstream: a new mapping of a project to a distribution has been added

    Adding this rule will trigger notifications when a new mapping of a
    project to a distribution is **added** in `anitya
    <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.project.map.new')


@hint(topics=[_('anitya.project.map.update', prefix='org.release-monitoring')])
def anitya_mapping_update(config, message):
    """ Upstream: the mapping of a project to a distribution has been updated

    Adding this rule will trigger notifications when the mapping of a
    project to a distribution is **updated** in `anitya
    <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.project.map.update')


@hint(topics=[_('anitya.project.map.remove', prefix='org.release-monitoring')])
def anitya_mapping_deleted(config, message):
    """ Upstream: a mapping of a project to a distribution has been deleted

    Adding this rule will trigger notifications when the mapping of a
    project in a distribution is **deleted** in `anitya
    <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.project.map.remove')


@hint(topics=[_('anitya.project.remove', prefix='org.release-monitoring')])
def anitya_project_deleted(config, message):
    """ Upstream: a project is deleted

    Adding this rule will trigger notifications when a project is **deleted**
    to `anitya <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.project.remove')


@hint(topics=[_('anitya.project.version.update',
                prefix='org.release-monitoring')])
def anitya_new_update(config, message):
    """ Upstream: a project has an update

    Adding this rule will trigger notifications when a project has a
    **new release** according to `anitya <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.project.version.update')


@hint(topics=[_('anitya.project.update', prefix='org.release-monitoring')])
def anitya_info_update(config, message):
    """ Upstream: a project has been updated

    Adding this rule will trigger notifications when the information about
    a project are **updated** in `anitya <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.project.update')
