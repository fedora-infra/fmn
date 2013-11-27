def fedoratagger_rating_update(config, message):
    """ Fedoratagger: The rating of a package has been updated

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('fedoratagger.rating.update')


def fedoratagger_tag_create(config, message):
    """ Fedoratagger: A new tag has been added to a package

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('fedoratagger.tag.create')


def fedoratagger_tag_update(config, message):
    """ Fedoratagger: Someone voted on a tag

    TODO description for the web interface goes here
    """
    return message['topic'].endswith('fedoratagger.tag.update')
