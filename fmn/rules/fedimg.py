def fedimg_image_test(config, message):
    """ Fedimg: An image start state(started, completed, or failed)

    Adding this rule will let through notifications from the `Fedimg
    <https://github.com/fedora-infra/fedimg>`_ indicating the *image start
    state* (started, completed or failed).
    """
    return message['topic'].endswith('fedimg.image.test')


