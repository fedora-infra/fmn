# Generic filters for FMN

def user_filter(config, message, fasnick):
    """ Filters the messages by the user that performed the action.

    Use this filter to filter out messages that are associated with a
    specified user.
    """
    print config

    return fasnick in fedmsg.meta.msg2usernames(message)
