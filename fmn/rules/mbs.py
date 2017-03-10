from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['mbs'])
def mbs_catchall(config, message):
    """ All MBS events

    Adding this rule will indiscriminately match notifications of all types
    from the `module build service <https://mbs.fedoraproject.org>`_, i.e. every
    time any module build transitions to any state (init, wait, build, failed,
    completed, ready, ...)
    """
    return message['topic'].split('.')[3] == 'mbs'


@hint(topics=[_('mbs.module.state.change')])
def mbs_build_state_change(config, message):
    """ Module builds changing state (any state)

    This rule lets through messages from the `mbs build
    service <https://mbs.fedoraproject.org>`_ that get published anytime a
    build changes state.  The state could be anything:  started, completed,
    failed, etc...
    """
    return message['topic'].endswith('mbs.module.state.change')


@hint(topics=[_('buildsys.build.state.change')], invertible=False)
def mbs_build_started(config, message):
    """ Module builds submitted

    This rule lets through messages from the `module build
    service <https://mbs.fedoraproject.org>`_ that get published anytime **a
    module build starts**.
    """
    if not mbs_build_state_change(config, message):
        return False

    return message['msg']['state_name'] == 'wait'


@hint(topics=[_('buildsys.build.state.change')], invertible=False)
def mbs_build_completed(config, message):
    """ Module builds completing

    This rule lets through messages from the `module build
    service <https://mbs.fedoraproject.org>`_ that get published anytime **a
    module build completes**.
    """
    if not mbs_build_state_change(config, message):
        return False

    return message['msg']['state_name'] == 'done'


@hint(topics=[_('buildsys.build.state.change')], invertible=False)
def mbs_build_completed(config, message):
    """ Module builds failing

    This rule lets through messages from the `module build
    service <https://mbs.fedoraproject.org>`_ that get published anytime **a
    module build fails**.
    """
    if not mbs_build_state_change(config, message):
        return False

    return message['msg']['state_name'] == 'failed'
