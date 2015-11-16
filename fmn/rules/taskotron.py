from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('taskotron.result.new')])
def taskotron_result_new(config, message):
    """ New taskotron task result

    This rule lets through messages from the `taskotron
    <https://taskotron.fedoraproject.org>`_ about new task result.
    """
    return message['topic'].endswith('taskotron.result.new')

@hint(categories=['taskotron'], invertible=False)
def taskotron_task(config, message, task=None):
    """ Particular taskotron task

    With this rule, you can limit messages to only those of particular
    `taskotron https://taskotron.fedoraproject.org/`_ task.

    You can specify several tasks by separating them with a comma ',',
    i.e.: ``depcheck,rpmlint``.
    """

    if not task:
        return False

    tasks = [item.strip() for item in task.split(',')]
    return message['msg']['task'].get('name') in tasks
