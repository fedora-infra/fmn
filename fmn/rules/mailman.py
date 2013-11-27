def mailman_receive(config, message):
    """ Mailman: An email has been sent to a mailing list

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('mailman.receive')
