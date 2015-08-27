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


@hint(topics=[_('bodhi.update.complete.stable')])
def bodhi_update_complete_stable(config, message):
    """ When updates complete their requested push to "stable"

    This rule will let through messages from the backend of the `Bodhi Updates
    System <https://admin.fedoraproject.org/updates>`_ when it **completes**
    the process of mashing individual updates into a new stable repo.
    Separate messages are generated here for each update in the mash.
    """
    return message['topic'].endswith('bodhi.update.complete.stable')


@hint(topics=[_('bodhi.update.complete.testing')])
def bodhi_update_complete_testing(config, message):
    """ When updates complete their requested push to "testing"

    This rule will let through messages from the backend of the `Bodhi Updates
    System <https://admin.fedoraproject.org/updates>`_ when it **completes**
    the process of mashing individual updates into a new testing repo.
    Separate messages are generated here for each update in the mash.
    """
    return message['topic'].endswith('bodhi.update.complete.testing')


@hint(topics=[_('bodhi.update.eject')])
def bodhi_update_eject(config, message):
    """ When an update is ejected from the bodhi mash

    This rule will let through messages from the backend of the `Bodhi Updates
    System <https://admin.fedoraproject.org/updates>`_ when it **ejects** an
    update from the mash.  This is typically because something is determined
    to be faulty about the update (the request is inconsistent or it is
    failing some required taskotron checks).

    """
    return message['topic'].endswith('bodhi.update.eject')


@hint(topics=[_('bodhi.errata.publish')])
def bodhi_errata_publish(config, message):
    """ New errata about updates being mashed

    This rule will let through messages from the backend of the `Bodhi Updates
    System <https://admin.fedoraproject.org/updates>`_ when it finishes
    publishes errata about an update near the end of the mash.

    """
    return message['topic'].endswith('bodhi.errata.publish')


@hint(topics=[_('bodhi.masher.start')])
def bodhi_masher_start(config, message):
    """ Requests for a new Bodhi mash

    This rule will let through messages from the backend of the `Bodhi Updates
    System <https://admin.fedoraproject.org/updates>`_ when an admin requests a
    new run of the bodhi masher.
    """
    return message['topic'].endswith('bodhi.masher.start')


@hint(topics=[_('bodhi.mashtask.start')])
def bodhi_mashtask_start(config, message):
    """ Starts of internal bodhi backend mash tasks

    This rule will let through messages from the backend of the `Bodhi Updates
    System <https://admin.fedoraproject.org/updates>`_ when it begins work on a
    repo.
    """
    return message['topic'].endswith('bodhi.mashtask.start')


@hint(topics=[_('bodhi.mashtask.complete')])
def bodhi_mashtask_complete(config, message):
    """ Ends of internal bodhi backend mash tasks

    This rule will let through messages from the backend of the `Bodhi Updates
    System <https://admin.fedoraproject.org/updates>`_ when it finishes work on
    a repo.
    """
    return message['topic'].endswith('bodhi.mashtask.complete')


@hint(topics=[_('bodhi.mashtask.mashing')])
def bodhi_mashtask_mashing(config, message):
    """ Starts of the mash phase of the mashtask

    This rule will let through messages from the backend of the `Bodhi Updates
    System <https://admin.fedoraproject.org/updates>`_ when it starts the
    "mashing" phase of the mash task.

    """
    return message['topic'].endswith('bodhi.mashtask.mashing')


@hint(topics=[_('bodhi.mashtask.sync.wait')])
def bodhi_mashtask_sync_wait(config, message):
    """ When the masher waits for content to sync to the mirrors

    This rule will let through messages from the backend of the `Bodhi Updates
    System <https://admin.fedoraproject.org/updates>`_ when it starts the
    "sync.wait" phase of the mash task.

    """
    return message['topic'].endswith('bodhi.mashtask.sync.wait')


@hint(topics=[_('bodhi.mashtask.sync.done')])
def bodhi_mashtask_sync_done(config, message):
    """ When the masher confirms content is on the master mirror

    This rule will let through messages from the backend of the `Bodhi Updates
    System <https://admin.fedoraproject.org/updates>`_ when it finishes the
    "sync.wait" phase of the mash task.

    """
    return message['topic'].endswith('bodhi.mashtask.sync.done')
