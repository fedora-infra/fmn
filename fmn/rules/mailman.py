def mailman_receive(config, message):
    """ Mailman: An email has been sent to a mailing list

    Including this rule will trigger a notification anytime
    an **email is posted** to any Fedora Project **mailman3** list.

    If you're using this to send yourself emails, it might make more sense to
    just *subscribe to the list*... think about it.
    """
    return message['topic'].endswith('mailman.receive')
