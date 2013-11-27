

def buildsys_build_state_change(config, message):
    """ Buildsys: build changed state (started, failed, finished)

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('buildsys.build.state.change')


def buildsys_package_list_change(config, message):
    """ Buildsys: Package list changed

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('buildsys.package.list.change')


def buildsys_repo_done(config, message):
    """ Buildsys: Building a repo has finished

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('buildsys.repo.done')


def buildsys_repo_init(config, message):
    """ Buildsys: Building a repo has started

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('buildsys.repo.init')


def buildsys_tag(config, message):
    """ Buildsys: A package has been tagged

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('buildsys.tag')


def buildsys_untag(config, message):
    """ Buildsys: A package has been untagged

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('buildsys.untag')
