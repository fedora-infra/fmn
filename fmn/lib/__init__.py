""" fedmsg-notifications internal API """

import fmn.lib.models

import logging
log = logging.getLogger(__name__)


def recipients(session, config, message):
    """ The main API function.

    Accepts a fedmsg message as an argument.

    Returns a dict mapping context names to lists of recipients.
    """

    res = {}

    for context in session.query(fmn.lib.models.Context).all():
        res[context.name] = recipients_for_context(
            session, config, context, message)

    return res


def recipients_for_context(session, config, context, message):
    """ Returns the recipients for a given fedmsg message and stated context.

    Context may be either the name of a context or an instance of
    fmn.lib.models.Context.
    """

    if isinstance(context, basestring):
        context = session.query(fmn.lib.models.Context)\
            .filter_by(name=context).one()

    return context.recipients(session, config, message)


def load_filters(root='fmn.filters'):
    """ Load the big list of allowed callable filters. """

    module = __import__(root, fromlist=[root.split('.')[0]])

    filters = []
    for name in dir(module):
        obj = getattr(module, name)
        if not callable(obj):
            continue
        log.info("Found filter %r %r" % (name, obj))
        filters.append(obj)

    return filters
