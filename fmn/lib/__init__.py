""" fedmsg-notifications internal API """

import fmn.lib.models


def recipients(session, message):
    """ The main API function.

    Accepts a fedmsg message as an argument.

    Returns a dict mapping context names to lists of recipients.
    """

    res = {}

    for context in session.query(fmn.lib.models.Context).all():
        res[context.name] = recipients_for_context(session, context, message)

    return res


def recipients_for_context(session, context, message):
    """ Returns the recipients for a given fedmsg message and stated context.

    Context may be either the name of a context or an instance of
    fmn.lib.models.Context.
    """

    if isinstance(context, basestring):
        context = session.query(fmn.lib.models.Context)\
            .filter_by(name=context).one()

    return context.recipients(session, message)
