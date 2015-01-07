def jenkins_build_aborted(config, message):
    """ Jenkins: A build has been aborted

    Adding this rule to your filters will let through messages
    from `Jenkins <http://jenkins.cloud.fedoraproject.org/>`_
    when a build is **aborted**.
    """
    return message['topic'].endswith('jenkins.build.aborted')


def jenkins_build_failed(config, message):
    """ Jenkins: A build has failed

    Adding this rule to your filters will let through messages
    from `Jenkins <http://jenkins.cloud.fedoraproject.org/>`_
    when a build is **completed with failure**.
    """
    return message['topic'].endswith('jenkins.build.failed')


def jenkins_build_notbuilt(config, message):
    """ Jenkins: A build was not built

    Adding this rule to your filters will let through messages
    from `Jenkins <http://jenkins.cloud.fedoraproject.org/>`_
    when a build **doesn't actually build**.
    """
    return message['topic'].endswith('jenkins.build.notbuilt')


def jenkins_build_passed(config, message):
    """ Jenkins: A build was completed successfully

    Adding this rule to your filters will let through messages
    from `Jenkins <http://jenkins.cloud.fedoraproject.org/>`_
    when a build **completes successfully**.
    """
    return message['topic'].endswith('jenkins.build.passed')


def jenkins_build_start(config, message):
    """ Jenkins: A build has started

    Adding this rule to your filters will let through messages
    from `Jenkins <http://jenkins.cloud.fedoraproject.org/>`_
    when a build **starts**.
    """
    return message['topic'].endswith('jenkins.build.start')


def jenkins_build_unstable(config, message):
    """ Jenkins: A build has completed with warnings

    Adding this rule to your filters will let through messages
    from `Jenkins <http://jenkins.cloud.fedoraproject.org/>`_
    when a build **completes with warnings**.
    """
    return message['topic'].endswith('jenkins.build.unstable')


