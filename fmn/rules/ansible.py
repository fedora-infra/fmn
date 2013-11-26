

def playbook_complete(config, message):
    """ Playbook completed

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('ansible.playbook.complete')


def playbook_started(config, message):
    """ Playbook started

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('ansible.playbook.start')
