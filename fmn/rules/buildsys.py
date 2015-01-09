from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['buildsys'], invertible=False)
def koji_instance(config, message, instance=None, *args, **kw):
    """ Koji: pertains only to particular instances

    You may not have even known it, but we have multiple instances of the koji
    build system.  There is the **primary** buildsystem at
    `koji.fedoraproject.org <https://koji.fedoraproject.org>`_ and also
    secondary instances for `ppc <https://ppc.koji.fedoraproject.org>`_, `arm
    <https://arm.koji.fedoraproject.org>`_, and `s390
    <https://s390.koji.fedoraproject.org>`_.

    With this rule, you can limit messages to only those from particular koji
    instances (like the **primary** one if you want to ignore the secondary
    ones).  You should use this rule **in combination** with other koji rules
    so you get only a *certain subset* of messages from one instance.  You
    almost certainly do not want **all** messages from a given instance.

    You can specify several instances by separating them with a comma ',',
    i.e.: ``primary,ppc``.
    """

    instance = kw.get('instance', instance)
    if not instance:
        return False

    instances = [item.strip() for item in instance.split(',')]
    return message['msg'].get('instance') in instances


@hint(topics=[_('buildsys.task.state.change')])
def koji_scratch_build_state_change(config, message):
    """ Koji: *scratch* build changed state (started, failed, finished)

    This rule lets through messages from the `koji build
    system <https://koji.fedoraproject.org>`_ about **scratch** build state
    state changes (any state at all:  started, completed, failed, cancelled).
    """
    return message['topic'].endswith('buildsys.task.state.change')


@hint(topics=[_('buildsys.task.state.change')], invertible=False)
def koji_scratch_build_started(config, message):
    """ Koji: *scratch* build started

    This rule lets through messages from the `koji build
    system <https://koji.fedoraproject.org>`_ that get published anytime a
    **scratch** build starts.
    """
    if not koji_scratch_build_state_change(config, message):
        return False

    return message['msg']['new'] == 'OPEN'


@hint(topics=[_('buildsys.task.state.change')], invertible=False)
def koji_scratch_build_completed(config, message):
    """ Koji: *scratch* build completed

    This rule lets through messages from the `koji build
    system <https://koji.fedoraproject.org>`_ that get published anytime a
    **scratch** build completes.
    """
    if not koji_scratch_build_state_change(config, message):
        return False

    return message['msg']['new'] == 'CLOSED'


@hint(topics=[_('buildsys.task.state.change')], invertible=False)
def koji_scratch_build_failed(config, message):
    """ Koji: *scratch* build failed

    This rule lets through messages from the `koji build
    system <https://koji.fedoraproject.org>`_ that get published anytime a
    **scratch** build fails.
    """
    if not koji_scratch_build_state_change(config, message):
        return False

    return message['msg']['new'] == 'FAILED'


@hint(topics=[_('buildsys.task.state.change')], invertible=False)
def koji_scratch_build_cancelled(config, message):
    """ Koji: *scratch* build cancelled

    This rule lets through messages from the `koji build
    system <https://koji.fedoraproject.org>`_ that get published anytime a
    **scratch** build is cancelled.
    """
    if not koji_scratch_build_state_change(config, message):
        return False

    return message['msg']['new'] == 'CANCELED'


@hint(topics=[_('buildsys.build.state.change')])
def koji_build_state_change(config, message):
    """ Koji: build changed state (started, failed, finished)

    This rule lets through messages from the `koji build
    system <https://koji.fedoraproject.org>`_ that get published anytime a
    build changes state.  The state could be anything:  started, completed,
    deleted, failed, or cancelled.
    """
    return message['topic'].endswith('buildsys.build.state.change')


@hint(topics=[_('buildsys.build.state.change')], invertible=False)
def koji_build_started(config, message):
    """ Koji: build started

    This rule lets through messages from the `koji build
    system <https://koji.fedoraproject.org>`_ that get published anytime **a
    build starts**.
    """
    if not koji_build_state_change(config, message):
        return False

    return message['msg']['new'] == 0


@hint(topics=[_('buildsys.build.state.change')], invertible=False)
def koji_build_completed(config, message):
    """ Koji: build completed

    This rule lets through messages from the `koji build
    system <https://koji.fedoraproject.org>`_ that get published anytime **a
    build completes**.
    """
    if not koji_build_state_change(config, message):
        return False

    return message['msg']['new'] == 1


@hint(topics=[_('buildsys.build.state.change')], invertible=False)
def koji_build_deleted(config, message):
    """ Koji: build deleted

    This rule lets through messages from the `koji build
    system <https://koji.fedoraproject.org>`_ that get published anytime **a
    build is deleted**.
    """
    if not koji_build_state_change(config, message):
        return False

    return message['msg']['new'] == 2


@hint(topics=[_('buildsys.build.state.change')], invertible=False)
def koji_build_failed(config, message):
    """ Koji: build failed

    This rule lets through messages from the `koji build
    system <https://koji.fedoraproject.org>`_ that get published anytime **a
    build fails**.
    """
    if not koji_build_state_change(config, message):
        return False

    return message['msg']['new'] == 3


@hint(topics=[_('buildsys.build.state.change')], invertible=False)
def koji_build_cancelled(config, message):
    """ Koji: build cancelled

    This rule lets through messages from the `koji build
    system <https://koji.fedoraproject.org>`_ that get published anytime **a
    build is cancelled**.
    """
    if not koji_build_state_change(config, message):
        return False

    return message['msg']['new'] == 4


@hint(topics=[_('buildsys.package.list.change')])
def koji_package_list_change(config, message):
    """ Koji: Package listing has changed

    This rule lets through messages from the `koji build
    system <https://koji.fedoraproject.org>`_ indicating that the package
    listing for a tag has changed.
    """
    return message['topic'].endswith('buildsys.package.list.change')


@hint(topics=[_('buildsys.repo.done')])
def koji_repo_done(config, message):
    """ Koji: Building a repo has finished

    This rule lets through messages indicating that the `koji build
    system <https://koji.fedoraproject.org>`_ has **finished** rebuilding a
    repo.
    """
    return message['topic'].endswith('buildsys.repo.done')


@hint(topics=[_('buildsys.repo.init')])
def koji_repo_init(config, message):
    """ Koji: Building a repo has started

    This rule lets through messages indicating that the `koji build
    system <https://koji.fedoraproject.org>`_ has **started** rebuilding a
    repo.
    """
    return message['topic'].endswith('buildsys.repo.init')


@hint(topics=[_('buildsys.tag')])
def koji_tag(config, message):
    """ Koji: A package has been tagged

    This rule lets through messages that get published when the `koji build
    system <https://koji.fedoraproject.org>`_ applies a certain tag to a
    package.
    """
    return message['topic'].endswith('buildsys.tag')


@hint(topics=[_('buildsys.untag')])
def koji_untag(config, message):
    """ Koji: A package has been untagged

    This rule lets through messages that get published when the `koji build
    system <https://koji.fedoraproject.org>`_ removes a tag from a
    package.
    """
    return message['topic'].endswith('buildsys.untag')
