def github_commit_comment(config, message):
    """ Github: Someone commented directly on a commit

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **directly comments on a commit**.
    """
    return message['topic'].endswith('github.commit_comment')


def github_create(config, message):
    """ Github: Someone created a new tag or branch

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **creates a new tag or branch**.
    """
    return message['topic'].endswith('github.create')


def github_delete(config, message):
    """ Github: Someone deleted a tag or branch

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **deletes a tag or branch**.
    """
    return message['topic'].endswith('github.delete')


def github_fork(config, message):
    """ Github: Someone forked a repo

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **forks a repo**.
    """
    return message['topic'].endswith('github.fork')


def github_issue_comment(config, message):
    """ Github: Someone commented on an issue

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **comments on an issue** for an enabled repository.
    """
    return message['topic'].endswith('github.issue.comment')


def github_issue_reopened(config, message):
    """ Github: Someone changed an issue

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **changes an issue** for an enabled repository.
    """
    return message['topic'].endswith('github.issue.reopened')


def github_pull_request_closed(config, message):
    """ Github: Someone closed an existing pull request

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **closed an existing pull request**.
    """
    return message['topic'].endswith('github.pull_request.closed')


def github_pull_request_review_comment(config, message):
    """ Github: Someone commented on a pull request

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **comments on a pull request**.
    """
    return message['topic'].endswith('github.pull_request_review_comment')


def github_push(config, message):
    """ Github: Someone pushed to a github repo

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **pushes** to an enabled github repository.
    """
    return message['topic'].endswith('github.push')


def github_status(config, message):
    """ Github: CI service updated the status of new commit

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when **continuous integration service updates the status of a new
    commit.**
    """
    return message['topic'].endswith('github.status')


def github_watch(config, message):
    """ Github: Someone started watching a repository

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **watches** a repository.
    """
    return message['topic'].endswith('github.watch')


def github_webhook(config, message):
    """ Github: Someone enabled hook for fedmsg broadcast on a repository

    Adding this rule to your filters will let through messages
    from `Github <https://apps.fedoraproject.org/github2fedmsg>`_
    when someone **enables a new repository for fedmsg broadcast**.
    """
    return message['topic'].endswith('github.webhook')


