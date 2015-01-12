from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['anitya'])
def anitya_catchall(config, message):
    """ All release-monitoring.org events

    Adding this rule will indiscriminately match notifications of all types
    from `release-monitoring.org <https://release-monitoring.org>`_ (also
    called "anitya"), i.e. notices of new upstream tarball releases, changes to
    package/project mappings, new distributions being added, etc..
    """
    return message['topic'].split('.')[3] == 'anitya'


@hint(topics=[_('anitya.distro.add', prefix='org.release-monitoring')])
def anitya_distro_add(config, message):
    """ New distributions added to release-monitoring.org

    Adding this rule will trigger notifications when a new distribution is
    **added** to `anitya <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.distro.add')


@hint(topics=[_('anitya.distro.edit', prefix='org.release-monitoring')])
def anitya_distro_update(config, message):
    """ Anitya distributions updated

    Adding this rule will trigger notifications when a distribution is
    **updated** in `anitya <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.distro.edit')


@hint(topics=[_('anitya.project.add', prefix='org.release-monitoring')])
def anitya_project_add(config, message):
    """ New projects added to release-monitoring.org

    Adding this rule will trigger notifications when a project is **added**
    to `anitya <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.project.add')


@hint(topics=[_('anitya.project.add.tried', prefix='org.release-monitoring')])
def anitya_project_add_tried(config, message):
    """ Attempts to add new projects to release-monitoring.org

    Adding this rule will trigger notifications when a project is tried to
    be **added** to `anitya <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.project.add.tried')


@hint(topics=[_('anitya.project.edit', prefix='org.release-monitoring')])
def anitya_project_update(config, message):
    """ Updates to projects on release-monitoring.org

    Adding this rule will trigger notifications when a project is **updated**
    in `anitya <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.project.edit')


@hint(topics=[_('anitya.project.map.new', prefix='org.release-monitoring')])
def anitya_mapping_new(config, message):
    """ When upstream projects are mapped to downstream packages

    Adding this rule will trigger notifications when a new mapping of a
    project to a distribution is **added** in `anitya
    <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.project.map.new')


@hint(topics=[_('anitya.project.map.update', prefix='org.release-monitoring')])
def anitya_mapping_update(config, message):
    """ Updates to anitya's upstream/downstream mappings

    Adding this rule will trigger notifications when the mapping of a
    project to a distribution is **updated** in `anitya
    <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.project.map.update')


@hint(topics=[_('anitya.project.map.remove', prefix='org.release-monitoring')])
def anitya_mapping_deleted(config, message):
    """ When upstream/downstream mappings are deleted

    Adding this rule will trigger notifications when the mapping of a
    project in a distribution is **deleted** in `anitya
    <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.project.map.remove')


@hint(topics=[_('anitya.project.remove', prefix='org.release-monitoring')])
def anitya_project_deleted(config, message):
    """ When upstream projects are deleted from anitya

    Adding this rule will trigger notifications when a project is **deleted**
    to `anitya <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.project.remove')


@hint(topics=[_('anitya.project.version.update',
                prefix='org.release-monitoring')])
def anitya_new_update(config, message):
    """ When new upstream releases are detected

    Adding this rule will trigger notifications when a project has a
    **new release** according to `anitya <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.project.version.update')


@hint(topics=[_('anitya.project.update', prefix='org.release-monitoring')])
def anitya_info_update(config, message):
    """ When an upstream project's metadata is updated

    Adding this rule will trigger notifications when the information about
    a project are **updated** in `anitya <release-monitoring.org>`_.
    """
    return message['topic'].endswith('anitya.project.update')
