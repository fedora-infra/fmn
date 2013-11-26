""" Fedora Notifications internal API """

import fmn.lib.models

import inspect
import logging

import docutils.examples
import markupsafe

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

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


def load_rules(root='fmn.rules'):
    """ Load the big list of allowed callable rules. """

    module = __import__(root, fromlist=[root.split('.')[0]])

    rules = {}
    for name in dir(module):
        obj = getattr(module, name)
        if not callable(obj):
            continue
        log.info("Found rule %r %r" % (name, obj))

        doc = inspect.getdoc(obj)

        # It's crazy, but inspect (stdlib!) doesn't return unicode objs.
        if doc:
            doc = doc.decode('utf-8')

        if doc:
            title, doc_as_rst = doc.split('\n', 1)
            doc = docutils.examples.html_parts(doc_as_rst)['body']
            doc = markupsafe.Markup(doc)
        else:
            title = "UNDOCUMENTED"
            doc = "No docs for %s:%s %r" % (root, name, obj)

        rules[name] = {
            'func': obj,
            'title': title.strip(),
            'doc': doc.strip(),
            'args': inspect.getargspec(obj)[0],
        }

    rules = OrderedDict(
        sorted(rules.items(), key=lambda x: x[1]['title'])
    )

    return {root: rules}
