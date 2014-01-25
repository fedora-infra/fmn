""" Fedora Notifications internal API """

import fmn.lib.models

import inspect
import logging
import re

import bs4
import docutils.examples
import markupsafe

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

log = logging.getLogger(__name__)

irc_regex = r'[a-zA-Z_\-\[\]\\^{}|`][a-zA-Z0-9_\-\[\]\\^{}|`]*'
email_regex = r'^([a-zA-Z0-9_\-\.]+)@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$'
gcm_regex = r'^[\w-]+$'


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
        log.debug("Found rule %r %r" % (name, obj))

        doc = inspect.getdoc(obj)

        # It's crazy, but inspect (stdlib!) doesn't return unicode objs.
        if doc:
            doc = doc.decode('utf-8')

        if doc:
            # If we have a docstring, then mark it up beautifully for display
            # in the web app.
            # FWIW, this should probably be moved into fmn.web since nowhere
            # else are we going to want HTML... we'll still want raw .rst.
            title, doc_as_rst = doc.split('\n', 1)
            doc = docutils.examples.html_parts(doc_as_rst)['body']
            soup = bs4.BeautifulSoup(doc)
            doc_no_links = ''.join(map(unicode, strip_anchor_tags(soup)))
            doc = markupsafe.Markup(doc)
            doc_no_links = markupsafe.Markup(doc_no_links)
        else:
            title = "UNDOCUMENTED"
            doc = "No docs for %s:%s %r" % (root, name, obj)
            doc_no_links = doc

        rules[name] = {
            'func': obj,
            'title': title.strip(),
            'doc': doc.strip(),
            'doc-no-links': doc_no_links.strip(),
            'args': inspect.getargspec(obj)[0],
        }

    rules = OrderedDict(
        sorted(rules.items(), key=lambda x: x[1]['title'])
    )

    return {root: rules}


def strip_anchor_tags(soup):
    for tag in soup.contents:
        if isinstance(tag, bs4.Tag) and tag.name not in ('a'):
            tag.contents = list(strip_anchor_tags(tag))
            yield tag
        elif isinstance(tag, bs4.Tag) and tag.name in ('a'):
            yield tag.string
        else:
            yield tag


def validate_detail_value(ctx, value):
    if ctx.name == 'irc':
        if re.match(irc_regex, value) is None:
            raise ValueError("value must be a valid irc nick")
    elif ctx.name == 'email':
        if re.match(email_regex, value) is None:
            raise ValueError("value must be an email address")
    elif ctx.name == 'android':
        if re.match(gcm_regex, value) is None:
            raise ValueError("not a valid android registration id")
    else:
        raise NotImplementedError("No validation scheme for %r" % ctx.name)
    # Happy.
    return
