""" fedmsg-notifications internal API """

import fmn.lib.models

import collections
import inspect
import logging
log = logging.getLogger(__name__)


def recipients(session, config, valid_paths, message):
    """ The main API function.

    Accepts a fedmsg message as an argument.

    Returns a dict mapping context names to lists of recipients.
    """

    res = {}

    for context in session.query(fmn.lib.models.Context).all():
        res[context.name] = recipients_for_context(
            session, config, valid_paths, context, message)

    return res


def recipients_for_context(session, config, valid_paths, context, message):
    """ Returns the recipients for a given fedmsg message and stated context.

    Context may be either the name of a context or an instance of
    fmn.lib.models.Context.
    """

    if isinstance(context, basestring):
        context = session.query(fmn.lib.models.Context)\
            .filter_by(name=context).one()

    return context.recipients(session, config, valid_paths, message)


def load_filters(root='fmn.filters'):
    """ Load the big list of allowed callable filters. """

    module = __import__(root, fromlist=[root.split('.')[0]])

    filters = {}
    for name in dir(module):
        obj = getattr(module, name)
        if not callable(obj):
            continue
        log.info("Found filter %r %r" % (name, obj))

        doc = inspect.getdoc(obj)
        if doc:
            title, doc = doc.split('\n', 1)
        else:
            title = "UNDOCUMENTED"
            doc = "No docs for %s:%s %r" % (root, name, obj)

        filters[name] = {
            'func': obj,
            'title': title.strip(),
            'doc': doc.strip(),
            'args': inspect.getargspec(obj)[0],
        }

    filters = collections.OrderedDict(
        sorted(filters.items(), key=lambda x: x[1]['title'])
    )

    return {root: filters}
