from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('kerneltest.release.edit')])
def kerneltest_release_edit(config, message):
    """ An admin edits an existing release (kerneltest)

    Adding this rule to your filters will let through messages
    from `Kernel Test <https://apps.fedoraproject.org/kerneltest>`_
    when an admin **edits** an existing release.
    """
    return message['topic'].endswith('kerneltest.release.edit')


@hint(topics=[_('kerneltest.release.new')])
def kerneltest_release_new(config, message):
    """ An admin adds a new release (kerneltest)

    Adding this rule to your filters will let through messages
    from `Kernel Test <https://apps.fedoraproject.org/kerneltest>`_
    when an admin **sets up** an existing release.
    """
    return message['topic'].endswith('kerneltest.release.new')


@hint(topics=[_('kerneltest.upload.new')])
def kerneltest_upload_new(config, message):
    """ New kerneltest test results

    Adding this rule to your filters will let through messages
    from `Kernel Test <https://apps.fedoraproject.org/kerneltest>`_
    when a new test result is uploaded.
    """
    return message['topic'].endswith('kerneltest.upload.new')
