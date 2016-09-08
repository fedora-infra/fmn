from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('taskotron.result.new')])
def taskotron_result_new(config, message, **kwargs):
    """ New taskotron task result

    This rule lets through messages from the `taskotron
    <https://taskotron.fedoraproject.org>`_ about new task result.
    """
    return message['topic'].endswith('taskotron.result.new')


@hint(categories=['taskotron'], invertible=False)
def taskotron_task(config, message, task=None):
    """ Particular taskotron task

    With this rule, you can limit messages to only those of particular
    `taskotron <https://taskotron.fedoraproject.org/>`_ task.

    You can specify several tasks by separating them with a comma ',',
    i.e.: ``dist.depcheck,dist.rpmlint``.
    """

    # We only operate on taskotron messages, first off.
    if not taskotron_result_new(config, message):
        return False

    if not task:
        return False

    tasks = [item.strip().lower() for item in task.split(',')]
    return message['msg']['task'].get('name').lower() in tasks


@hint(categories=['taskotron'], invertible=False)
def taskotron_changed_outcome(config, message):
    """ Taskotron task outcome changed

    With this rule, you can limit messages to only those task results
    with changed outcomes. This is useful when an object (a build,
    an update, etc) gets retested and either the object itself or the
    environment changes and the task outcome is now different (e.g.
    FAILED -> PASSED).
    """

    # We only operate on taskotron messages, first off.
    if not taskotron_result_new(config, message):
        return False

    outcome = message['msg']['result'].get('outcome')
    prev_outcome = message['msg']['result'].get('prev_outcome')

    return prev_outcome is not None and outcome != prev_outcome


@hint(categories=['taskotron'], invertible=False)
def taskotron_task_outcome(config, message, outcome=None):
    """ Particular taskotron task outcome

    With this rule, you can limit messages to only those of particular
    `taskotron <https://taskotron.fedoraproject.org/>`_ task outcome.

    You can specify several outcomes by separating them with a comma ',',
    i.e.: ``PASSED,FAILED``.

    The full list of supported outcomes can be found in the libtaskotron
    `documentation <https://docs.qadevel.cloud.fedoraproject.org/
    libtaskotron/latest/resultyaml.html#minimal-version>`_.
    """

    # We only operate on taskotron messages, first off.
    if not taskotron_result_new(config, message):
        return False

    if not outcome:
        return False

    outcomes = [item.strip().lower() for item in outcome.split(',')]
    return message['msg']['result'].get('outcome').lower() in outcomes


@hint(categories=['taskotron'], invertible=False)
def taskotron_task_particular_or_changed_outcome(config, message,
                                                 outcome='FAILED,NEEDS_INSPECTION'):
    """ Taskotron task any particular or changed outcome(s)

    With this rule, you can limit messages to only those task results
    with any particular outcome(s) (FAILED and NEEDS_INSPECTION by default)
    or those with changed outcomes. This rule is a handy way of filtering
    a very useful use case - being notified when either task requires
    your attention or the outcome has changed since the last time the task
    ran for the same item (e.g. a koji build).

    You can specify several outcomes by separating them with a comma ',',
    i.e.: ``PASSED,FAILED``.

    The full list of supported outcomes can be found in the libtaskotron
    `documentation <https://docs.qadevel.cloud.fedoraproject.org/
    libtaskotron/latest/resultyaml.html#minimal-version>`_.
    """

    return taskotron_task_outcome(config, message, outcome) or \
           taskotron_changed_outcome(config, message)


@hint(categories=['taskotron'], invertible=False)
def taskotron_release_critical_task(config, message):
    """ Release-critical taskotron tasks

    With this rule, you can limit messages to only those of
    release-critical
    `taskotron <https://taskotron.fedoraproject.org/>`_ task.

    These are the tasks which are deemed extremely important
    by the distribution, and their failure should be carefully
    inspected. Currently these tasks are ``dist.depcheck`` and
    ``dist.upgradepath``.
    """

    # We only operate on taskotron messages, first off.
    if not taskotron_result_new(config, message):
        return False

    task = message['msg']['task'].get('name')

    return task in ['dist.depcheck', 'dist.upgradepath']
