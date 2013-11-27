def planet_post_new(config, message):
    """ Planet: A user posted on the Fedora planet

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('planet.post.new')
