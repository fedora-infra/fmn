

def playbook_complete(config, message):
    """ TODO description for the web interface goes here
    """
    return message['topic'].endswith('ansible.playbook.complete')


def playbook_started(config, message):
    """ TODO description for the web interface goes here
    """
    return message['topic'].endswith('ansible.playbook.start')
