from fmn.lib.hinting import hint, prefixed as _


@hint(categories=['github'])
def github_catchall(config, message):
    """ All Fedora-related GitHub activity

    Adding this rule will indiscriminately match notifications of all types
    from `github <https://github.com>`_ (but only the repositories that are
    mapped to Fedora via the `github2fedmsg service
    <https://apps.fedoraproject.org/github2fedmsg>`_).
    """
    return message['topic'].split('.')[3] == 'github'


@hint(topics=[_('github.commit_comment')])
def github_commit_comment(config, message):
    """ Commit comments (github.com)

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **directly comments on a commit**.
    """
    return message['topic'].endswith('github.commit_comment')


@hint(topics=[_('github.create')])
def github_create(config, message):
    """ New tags and branches (github.com)

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **creates a new tag or branch**.
    """
    return message['topic'].endswith('github.create')


@hint(topics=[_('github.delete')])
def github_delete(config, message):
    """ Deleted tags and branches (github.com)

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **deletes a tag or branch**.
    """
    return message['topic'].endswith('github.delete')


@hint(topics=[_('github.fork')])
def github_fork(config, message):
    """ Forked repos (github.com)

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **forks a repo**.
    """
    return message['topic'].endswith('github.fork')


@hint(topics=[_('github.issue.comment')])
def github_issue_comment(config, message):
    """ Issue comments (github.com)

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **comments on an issue** for an enabled repository.
    """
    return message['topic'].endswith('github.issue.comment')


@hint(topics=[_('github.issue.reopened')])
def github_issue_reopened(config, message):
    """ Reopened issues (github.com)

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **changes an issue** for an enabled repository.
    """
    return message['topic'].endswith('github.issue.reopened')


@hint(topics=[_('github.pull_request.closed')])
def github_pull_request_closed(config, message):
    """ Closed pull-requests (github.com)

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **closed an existing pull request**.
    """
    return message['topic'].endswith('github.pull_request.closed')


@hint(topics=[_('github.pull_request_review_comment')])
def github_pull_request_review_comment(config, message):
    """ Pull-request review comments (github.com)

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **comments on a pull request**.
    """
    return message['topic'].endswith('github.pull_request_review_comment')


@hint(topics=[_('github.push')])
def github_push(config, message):
    """ Git pushes (github.com)

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **pushes** to an enabled github repository.
    """
    return message['topic'].endswith('github.push')


@hint(topics=[_('github.status')])
def github_status(config, message):
    """ Continuous integration status (github.com)

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when **continuous integration service updates the status of a new
    commit.**
    """
    return message['topic'].endswith('github.status')


@hint(topics=[_('github.watch')])
def github_watch(config, message):
    """ Users watching repos (github.com)

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **watches** a repository.
    """
    return message['topic'].endswith('github.watch')


@hint(topics=[_('github.webhook')])
def github_webhook(config, message):
    """ New github repos on the fedmsg bus

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **enables a new repository for fedmsg broadcast**.
    """
    return message['topic'].endswith('github.webhook')
