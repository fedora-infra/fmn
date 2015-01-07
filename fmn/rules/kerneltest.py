def kerneltest_release_edit(config, message):
    """ Kernel Test: An admin edited an existing release

    Adding this rule to your filters will let through messages
    from `Kernel Test <https://apps.fedoraproject.org/kerneltest>`_
    when an admin **edits** an existing release.
    """
    return message['topic'].endswith('kerneltest.release.edit')


def kerneltest_release_new(config, message):
    """ Kernel Test: An admin did set up an existing release

    Adding this rule to your filters will let through messages
    from `Kernel Test <https://apps.fedoraproject.org/kerneltest>`_
    when an admin **sets up** an existing release.
    """
    return message['topic'].endswith('kerneltest.release.new')


def kerneltest_upload_new(config, message):
    """ Kernel Test: A new test result was uploaded

    Adding this rule to your filters will let through messages
    from `Kernel Test <https://apps.fedoraproject.org/kerneltest>`_
    when a new test result is uploaded.
    """
    return message['topic'].endswith('kerneltest.upload.new')


