from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('fedimg.image.test')])
def fedimg_image_test_state(config, message):
    """ Fedimg: An image test state (started, completed, or failed)

    Adding this rule will let through notifications from the `Fedimg
    <https://github.com/fedora-infra/fedimg>`_ indicating the *image
    test state* (started, completed or failed).
    """
    return message['topic'].endswith('fedimg.image.test')


@hint(topics=[_('fedimg.image.test')], invertible=False)
def fedimg_image_test_started(config, message):
    """ Fedimg: An image test has started

    Adding this rule will let through notifications from the `Fedimg
    <https://github.com/fedora-infra/fedimg>`_ indicating the *image
    test* has started.
    """
    if not fedimg_image_test_state(config, message):
        return False

    return message['msg']['status'] == 'started'


@hint(topics=[_('fedimg.image.test')], invertible=False)
def fedimg_image_test_completed(config, message):
    """ Fedimg: An image test has completed

    Adding this rule will let through notifications from the `Fedimg
    <https://github.com/fedora-infra/fedimg>`_ indicating the *image
    test* has completed.
    """
    if not fedimg_image_test_state(config, message):
        return False

    return message['msg']['status'] == 'completed'


@hint(topics=[_('fedimg.image.test')], invertible=False)
def fedimg_image_test_failed(config, message):
    """ Fedimg: An image test has failed

    Adding this rule will let through notifications from the `Fedimg
    <https://github.com/fedora-infra/fedimg>`_ indicating the *image
    test* has failed.
    """
    if not fedimg_image_test_state(config, message):
        return False

    return message['msg']['status'] == 'failed'


@hint(topics=[_('fedimg.image.upload')])
def fedimg_image_upload_state(config, message):
    """ Fedimg: An image upload state (started, completed, or failed)

    Adding this rule will let through notifications from the `Fedimg
    <https://github.com/fedora-infra/fedimg>`_ indicating the *image
    upload state* (started, completed or failed).
    """
    return message['topic'].endswith('fedimg.image.upload')


@hint(topics=[_('fedimg.image.upload')], invertible=False)
def fedimg_image_upload_started(config, message):
    """ Fedimg: An image upload has started

    Adding this rule will let through notifications from the `Fedimg
    <https://github.com/fedora-infra/fedimg>`_ indicating the *image
    upload* has started.
    """
    if not fedimg_image_upload_state(config, message):
        return False

    return message['msg']['status'] == 'started'


@hint(topics=[_('fedimg.image.upload')], invertible=False)
def fedimg_image_upload_completed(config, message):
    """ Fedimg: An image upload has completed

    Adding this rule will let through notifications from the `Fedimg
    <https://github.com/fedora-infra/fedimg>`_ indicating the *image
    upload* has completed.
    """
    if not fedimg_image_upload_state(config, message):
        return False

    return message['msg']['status'] == 'completed'


@hint(topics=[_('fedimg.image.upload')], invertible=False)
def fedimg_image_upload_failed(config, message):
    """ Fedimg: An image upload has failed

    Adding this rule will let through notifications from the `Fedimg
    <https://github.com/fedora-infra/fedimg>`_ indicating the *image
    upload* has completed.
    """
    if not fedimg_image_upload_state(config, message):
        return False

    return message['msg']['status'] == 'failed'
