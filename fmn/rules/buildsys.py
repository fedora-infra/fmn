

def koji_build_state_change(config, message):
    """ Koji: build changed state (started, failed, finished)

    This rule lets through messages from the `koji build
    system <https://koji.fedoraproject.org>`_ that get published anytime a
    build changes state.  The state could be anything:  started, completed,
    deleted, failed, or cancelled.
    """
    return message['topic'].endswith('koji.build.state.change')


def koji_build_started(config, message):
    """ Koji: build started

    This rule lets through messages from the `koji build
    system <https://koji.fedoraproject.org>`_ that get published anytime **a
    build starts**.
    """
    if not koji_build_state_change(config, message):
        return False

    return message['msg']['new'] == 0


def koji_build_completed(config, message):
    """ Koji: build completed

    This rule lets through messages from the `koji build
    system <https://koji.fedoraproject.org>`_ that get published anytime **a
    build completes**.
    """
    if not koji_build_state_change(config, message):
        return False

    return message['msg']['new'] == 1


def koji_build_deleted(config, message):
    """ Koji: build deleted

    This rule lets through messages from the `koji build
    system <https://koji.fedoraproject.org>`_ that get published anytime **a
    build is deleted**.
    """
    if not koji_build_state_change(config, message):
        return False

    return message['msg']['new'] == 2


def koji_build_failed(config, message):
    """ Koji: build failed

    This rule lets through messages from the `koji build
    system <https://koji.fedoraproject.org>`_ that get published anytime **a
    build fails**.
    """
    if not koji_build_state_change(config, message):
        return False

    return message['msg']['new'] == 3


def koji_build_cancelled(config, message):
    """ Koji: build cancelled

    This rule lets through messages from the `koji build
    system <https://koji.fedoraproject.org>`_ that get published anytime **a
    build is cancelled**.
    """
    if not koji_build_state_change(config, message):
        return False

    return message['msg']['new'] == 4


def koji_repo_done(config, message):
    """ Koji: Building a repo has finished

    This rule lets through messages indicating that the `koji build
    system <https://koji.fedoraproject.org>`_ has **finished** rebuilding a
    repo.
    """
    return message['topic'].endswith('koji.repo.done')


def koji_repo_init(config, message):
    """ Koji: Building a repo has started

    This rule lets through messages indicating that the `koji build
    system <https://koji.fedoraproject.org>`_ has **started** rebuilding a
    repo.
    """
    return message['topic'].endswith('koji.repo.init')


def koji_tag(config, message):
    """ Koji: A package has been tagged

    This rule lets through messages that get published when the `koji build
    system <https://koji.fedoraproject.org>`_ applies a certain tag to a
    package.
    """
    return message['topic'].endswith('koji.tag')


def koji_untag(config, message):
    """ Koji: A package has been untagged

    This rule lets through messages that get published when the `koji build
    system <https://koji.fedoraproject.org>`_ removes a tag from a
    package.
    """
    return message['topic'].endswith('koji.untag')
