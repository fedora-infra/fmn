from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('jenkins.build.aborted')])
def jenkins_build_aborted(config, message):
    """ Jenkins builds abort

    Adding this rule to your filters will let through messages
    from `Jenkins <http://jenkins.cloud.fedoraproject.org/>`_
    when a build is **aborted**.
    """
    return message['topic'].endswith('jenkins.build.aborted')


@hint(topics=[_('jenkins.build.failed')])
def jenkins_build_failed(config, message):
    """ Jenkins builds that fail

    Adding this rule to your filters will let through messages
    from `Jenkins <http://jenkins.cloud.fedoraproject.org/>`_
    when a build is **completed with failure**.
    """
    return message['topic'].endswith('jenkins.build.failed')


@hint(topics=[_('jenkins.build.notbuilt')])
def jenkins_build_notbuilt(config, message):
    """ Jenkins builds that become "notbuilt"

    Adding this rule to your filters will let through messages
    from `Jenkins <http://jenkins.cloud.fedoraproject.org/>`_
    when a build **doesn't actually build**.
    """
    return message['topic'].endswith('jenkins.build.notbuilt')


@hint(topics=[_('jenkins.build.passed')])
def jenkins_build_passed(config, message):
    """ Jenkins builds that finish

    Adding this rule to your filters will let through messages
    from `Jenkins <http://jenkins.cloud.fedoraproject.org/>`_
    when a build **completes successfully**.
    """
    return message['topic'].endswith('jenkins.build.passed')


@hint(topics=[_('jenkins.build.start')])
def jenkins_build_start(config, message):
    """ Jenkins builds starting

    Adding this rule to your filters will let through messages
    from `Jenkins <http://jenkins.cloud.fedoraproject.org/>`_
    when a build **starts**.
    """
    return message['topic'].endswith('jenkins.build.start')


@hint(topics=[_('jenkins.build.unstable')])
def jenkins_build_unstable(config, message):
    """ Jenkins builds that finish with warnings

    Adding this rule to your filters will let through messages
    from `Jenkins <http://jenkins.cloud.fedoraproject.org/>`_
    when a build **completes with warnings**.
    """
    return message['topic'].endswith('jenkins.build.unstable')
