

def askbot_post_deleted(config, message):
    """ TODO description for the web interface goes here
    """
    return message['topic'].endswith('askbot.post.delete')


def askbot_post_edited(config, message):
    """ TODO description for the web interface goes here
    """
    return message['topic'].endswith('askbot.post.edit')


def askbot_post_flagged_offensive(config, message):
    """ TODO description for the web interface goes here
    """
    return message['topic'].endswith('askbot.post.flag_offensive.add')


def askbot_post_unflagged_offensive(config, message):
    """ TODO description for the web interface goes here
    """
    return message['topic'].endswith('askbot.post.flag_offensive.delete')


def askbot_tag_update(config, message):
    """ TODO description for the web interface goes here
    """
    return message['topic'].endswith('askbot.tag.update')
