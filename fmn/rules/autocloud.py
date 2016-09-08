from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('autocloud.compose.queued')])
def autocloud_compose_test_queued(config, message):
    """ Autocloud: A compose has been queued for testing

    Adding this rule will let through notifications from the
    `Autocloud <https://apps.fedoraproject.org/autocloud/>`
    indicating the *compose test* has been queued.
    """
    return message['topic'].endswith('autocloud.compose.queued')


@hint(topics=[_('autocloud.compose.running')])
def autocloud_compose_test_running(config, message):
    """ Autocloud: The tests for the compose are running

    Adding this rule will let through notifications from the
    `Autocloud <https://apps.fedoraproject.org/autocloud/>`
    indicating the *compose test* has started running.
    """
    return message['topic'].endswith('autocloud.compose.running')


@hint(topics=[_('autocloud.compose.complete')])
def autocloud_compose_test_completed(config, message):
    """ Autocloud: The tests for the compose has completed

    Adding this rule will let through notifications from the
    `Autocloud <https://apps.fedoraproject.org/autocloud/>`
    indicating the *compose test* has completed.
    """
    return message['topic'].endswith('autocloud.compose.complete')


@hint(topics=[_('autocloud.image.failed')])
def autocloud_image_test_failed(config, message):
    """ Autocloud: The tests for an image failed

    Adding this rule will let through notifications from the
    `Autocloud <https://apps.fedoraproject.org/autocloud/>`
    indicating the tests for an *image* failed.
    """
    return message['topic'].endswith('autocloud.image.failed')


@hint(topics=[_('autocloud.image.queued')])
def autocloud_image_test_queued(config, message):
    """ Autocloud: The image is queued for testing

    Adding this rule will let through notifications from the
    `Autocloud <https://apps.fedoraproject.org/autocloud/>`
    indicating the *image* is queued for testing.
    """
    return message['topic'].endswith('autocloud.image.queued')


@hint(topics=[_('autocloud.image.running')])
def autocloud_image_test_running(config, message):
    """ Autocloud: The tests for the image is running

    Adding this rule will let through notifications from the
    `Autocloud <https://apps.fedoraproject.org/autocloud/>`
    indicating the tests for the *image* is running.
    """
    return message['topic'].endswith('autocloud.image.running')


@hint(topics=[_('autocloud.image.success')])
def autocloud_image_test_success(config, message):
    """ Autocloud: The test for the image completed successfully

    Adding this rule will let through notifications from the
    `Autocloud <https://apps.fedoraproject.org/autocloud/>`
    indicating the tests for the *image* completed successfully.
    """
    return message['topic'].endswith('autocloud.image.success')
