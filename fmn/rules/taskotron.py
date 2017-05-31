from fmn.lib.hinting import hint, prefixed as _
import fnmatch


RELEASE_CRITICAL_TASKS = [
    # if you update this, don't forget to also update the docstring for
    # taskotron_release_critical_task()
    'dist.abicheck',
    'dist.rpmdeplint',
    'dist.upgradepath',
]


@hint(topics=[_('taskotron.result.new')])
def taskotron_result_new(config, message, **kwargs):
    """ New taskotron task result

    This rule lets through messages from the `taskotron
    <https://taskotron.fedoraproject.org>`_ about new task result.
    """
    return message['topic'].endswith('.taskotron.result.new')


@hint(categories=['taskotron'], invertible=False)
def taskotron_task(config, message, task=None):
    """ Particular taskotron task

    With this rule, you can limit messages to only those of particular
    `taskotron <https://taskotron.fedoraproject.org/>`_ task. Some tasks are
    documented on the `wiki <https://fedoraproject.org/wiki/Taskotron/Tasks>`_,
    and a full list of testcases (on which you can match) is visible in
    `resultsdb <https://taskotron.fedoraproject.org/resultsdb/testcases>`_.

    The match is case insensitive, and you can use shell-style wildcards (see
    `fnmatch <https://docs.python.org/2.7/library/fnmatch.html>`_), e.g.
    ``dist.rpmgrill*`` to match both ``dist.rpmgrill`` and all of its
    subresults (like ``dist.rpmgrill.man-pages``).

    You can specify several tasks by separating them with a comma ``,``,
    e.g.: ``dist.upgradepath,dist.rpmlint``.
    """

    # We only operate on taskotron messages, first off.
    if not taskotron_result_new(config, message):
        return False

    if not task:
        return False

    name = message['msg']['task'].get('name').lower()
    tasks = [item.strip().lower() for item in task.split(',')]

    for task in tasks:
        if task and fnmatch.fnmatchcase(name, task):
            return True

    return False


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

    return prev_outcome and outcome != prev_outcome


@hint(categories=['taskotron'], invertible=False)
def taskotron_task_outcome(config, message, outcome=None):
    """ Particular taskotron task outcome

    With this rule, you can limit messages to only those of particular
    `taskotron <https://taskotron.fedoraproject.org/>`_ task outcome.

    You can specify several outcomes by separating them with a comma ',',
    i.e.: ``PASSED,FAILED``.

    The full list of supported outcomes can be found in the libtaskotron
    `documentation <https://qa.fedoraproject.org/docs/libtaskotron/
    latest/resultyaml.html#minimal-version>`_.
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
    `documentation <https://qa.fedoraproject.org/docs/libtaskotron/
    latest/resultyaml.html#minimal-version>`_.
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
    inspected. Currently these tasks include::

    * ``dist.abicheck``
    * ``dist.rpmdeplint``
    * ``dist.upgradepath``
    """

    # We only operate on taskotron messages, first off.
    if not taskotron_result_new(config, message):
        return False

    task = message['msg']['task'].get('name')

    return task in RELEASE_CRITICAL_TASKS
