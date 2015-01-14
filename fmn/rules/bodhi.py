from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['bodhi'])
def bodhi_catchall(config, message):
    """ All bodhi events

    Adding this rule will indiscriminately match notifications of all types
    from the `Bodhi Updates System <https://admin.fedoraproject.org/updates>`_
    i.e. new updates, comments on updates, buildroot overrides, etc..
    """
    return message['topic'].split('.')[3] == 'bodhi'


@hint(categories=['bodhi'], invertible=False)
def bodhi_critpath(config, message):
    """ Critpath updates (of any kind)

    Adding this rule will allow through notifications about **critpath
    updates** from the `Bodhi Updates System
    <https://admin.fedoraproject.org/updates>`_.
    """
    return message['msg'].get('update', {}).get('critpath', False)


@hint(topics=[_('bodhi.buildroot_override.tag')])
def bodhi_buildroot_override_tag(config, message):
    """ New buildroot overrides

    Adding this rule will allow through notifications whenever a user
    **requests a buildroot override** via the `Bodhi Updates System
    <https://admin.fedoraproject.org/updates>`_.
    """
    return message['topic'].endswith('bodhi.buildroot_override.tag')


@hint(topics=[_('bodhi.buildroot_override.untag')])
def bodhi_buildroot_override_untag(config, message):
    """ Buildroot overrides being removed

    Adding this rule will allow through notifications whenever a user
    **delets a request for a buildroot override** via the `Bodhi Updates System
    <https://admin.fedoraproject.org/updates>`_.
    """
    return message['topic'].endswith('bodhi.buildroot_override.untag')


@hint(topics=[_('bodhi.update.comment')])
def bodhi_update_comment(config, message):
    """ Bodhi comments

    As part of the QA process, users may comment on updates in
    the `Bodhi Updates System <https://admin.fedoraproject.org/updates>`_.
    This rule will let through messages indicating that they have done so.
    """
    return message['topic'].endswith('bodhi.update.comment')


@hint(topics=[_('bodhi.update.request.obsolete')])
def bodhi_update_request_obsolete(config, message):
    """ Bodhi updates being obsoleted

    This rule will let through messages from the `Bodhi Updates System
    <https://admin.fedoraproject.org/updates>`_ indicating that a user has
    *requested* that an updated be **obsoleted**.
    """
    return message['topic'].endswith('bodhi.update.request.obsolete')


@hint(topics=[_('bodhi.update.request.revoke')])
def bodhi_update_request_revoke(config, message):
    """ Bodhi having their request revoked

    This rule will let through messages from the `Bodhi Updates System
    <https://admin.fedoraproject.org/updates>`_ indicating that a user has
    *requested* that an updated be **revoked**.
    """
    return message['topic'].endswith('bodhi.update.request.revoke')


@hint(topics=[_('bodhi.update.request.stable')])
def bodhi_update_request_stable(config, message):
    """ Requests for "stable" status on Bodhi updates

    This rule will let through messages from the `Bodhi Updates System
    <https://admin.fedoraproject.org/updates>`_ indicating that a user has
    *requested* that an updated be **pushed to stable**.
    """
    return message['topic'].endswith('bodhi.update.request.stable')


@hint(topics=[_('bodhi.update.request.testing')])
def bodhi_update_request_testing(config, message):
    """ New updates requested for updates-testing

    This rule will let through messages from the `Bodhi Updates System
    <https://admin.fedoraproject.org/updates>`_ indicating that a user has
    *requested* that an updated be **pushed to testing**.
    """
    return message['topic'].endswith('bodhi.update.request.testing')


@hint(topics=[_('bodhi.update.request.unpush')])
def bodhi_update_request_unpush(config, message):
    """ Requests for Bodhi updates to be unpushed

    This rule will let through messages from the `Bodhi Updates System
    <https://admin.fedoraproject.org/updates>`_ indicating that a user has
    *requested* that an updated be **unpushed**.
    """
    return message['topic'].endswith('bodhi.update.request.unpush')


@hint(topics=[_('bodhi.updates.epel.sync')])
def bodhi_update_epel_sync(config, message):
    """ New EPEL content has hit the master mirror

    This rule will let through messages from the `Bodhi Updates System
    <https://admin.fedoraproject.org/updates>`_ when new epel updates are
    synced out to the mirror master.
    """
    return message['topic'].endswith('bodhi.updates.epel.sync')


@hint(topics=[_('bodhi.updates.fedora.sync')])
def bodhi_update_fedora_sync(config, message):
    """ New Fedora updates content has hit the master mirror

    This rule will let through messages from the `Bodhi Updates System
    <https://admin.fedoraproject.org/updates>`_ when new fedora updates are
    synced out to the mirror master.
    """
    return message['topic'].endswith('bodhi.updates.fedora.sync')
