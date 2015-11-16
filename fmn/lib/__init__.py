""" Fedora Notifications internal API """

import fmn.lib.hinting
import fmn.lib.models

import inspect
import logging
import re
import smtplib

import bs4
import docutils.examples
import markupsafe
import six

from collections import defaultdict

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

log = logging.getLogger(__name__)

irc_regex = r'[a-zA-Z_\-\[\]\\^{}|`][a-zA-Z0-9_\-\[\]\\^{}|`]*'
gcm_regex = r'^[\w-]+$'


def recipients(preferences, message, valid_paths, config):
    """ The main API function.

    Accepts a fedmsg message as an argument.

    Returns a dict mapping context names to lists of recipients.
    """

    rule_cache = dict()
    results = defaultdict(list)
    notified = set()

    for preference in preferences:
        user = preference['user']
        context = preference['context']
        if (user['openid'], context['name']) in notified:
            continue

        for filter in preference['filters']:
            if matches(filter, message, valid_paths, rule_cache, config):
                for detail_value in preference['detail_values']:
                    results[context['name']].append({
                        'user': user['openid'],
                        context['detail_name']: detail_value,
                        'filter_name': filter['name'],
                        'filter_id': filter['id'],
                        'filter_oneshot': filter['oneshot'],
                        'markup_messages': preference['markup_messages'],
                        'triggered_by_links': preference['triggered_by_links'],
                        'shorten_links': preference['shorten_links'],
                        'verbose': preference['verbose'],
                    })
                notified.add((user['openid'], context['name']))
                break

    return results


def matches(filter, message, valid_paths, rule_cache, config):
    """ Returns True if the given filter matches the given message. """

    if not filter['rules']:
        return False

    for rule in filter['rules']:
        fn = rule['fn']
        negated = rule['negated']
        arguments = rule['arguments']
        rule_cache_key = rule['cache_key']

        try:
            if rule_cache_key not in rule_cache:
                value = fn(config, message, **arguments)
                if negated:
                    value = not value
                rule_cache[rule_cache_key] =  value

            if not rule_cache[rule_cache_key]:
                return False
        except Exception as e:
            log.exception(e)
            # If something throws an exception then we do *not* have a match.
            return False

    # Then all rules matched on this filter..
    return True


def load_preferences(session, config, valid_paths,
                     cull_disabled=False, openid=None,
                     cull_backends=None):
    """ Every rule for every filter for every context for every user.

    Any preferences in the DB that are for contexts that are disabled in the
    config are omitted here.

    If the `openid` argument is None, then this is an expensive query that
    loads, practically, the whole database.  However, if an openid string is
    submitted, then only the preferences of that user are returned (and this is
    less expensive).
    """

    cull_backends = cull_backends or []

    query = session.query(fmn.lib.models.Preference)

    if openid:
        query = query.filter(fmn.lib.models.Preference.openid==openid)

    preferences = query.all()
    return [
        preference.__json__(reify=True)
        for preference in preferences
        if (
            preference.context.name in config['fmn.backends']
            and preference.context.name not in cull_backends
            and (not cull_disabled or preference.enabled)
        )
    ]


def load_rules(root='fmn.rules'):
    """ Load the big list of allowed callable rules. """

    module = __import__(root, fromlist=[root.split('.')[0]])

    hinting_helpers = fmn.lib.hinting.__dict__.values()

    rules = {}
    for name in dir(module):
        obj = getattr(module, name)

        # Ignore non-callables.
        if not callable(obj):
            continue

        # Ignore our decorator and its friends
        if obj in hinting_helpers:
            continue

        doc = inspect.getdoc(obj)

        # It's crazy, but inspect (stdlib!) doesn't return unicode objs on py2.
        if doc and hasattr(doc, 'decode'):
            doc = doc.decode('utf-8')

        if doc:
            # If we have a docstring, then mark it up beautifully for display
            # in the web app.
            # FWIW, this should probably be moved into fmn.web since nowhere
            # else are we going to want HTML... we'll still want raw .rst.
            title, doc_as_rst = doc.split('\n', 1)
            doc = docutils.examples.html_parts(doc_as_rst)['body']
            soup = bs4.BeautifulSoup(doc, 'html5lib')
            doc_no_links = ''.join(map(six.text_type, strip_anchor_tags(soup)))
            doc = markupsafe.Markup(doc)
            doc_no_links = markupsafe.Markup(doc_no_links)
        else:
            title = "UNDOCUMENTED"
            doc = "No docs for %s:%s %r" % (root, name, obj)
            doc_no_links = doc

        rules[name] = {
            'func': obj,
            'submodule': obj.__module__.split('.')[-1],
            'title': title.strip(),
            'doc': doc.strip(),
            'doc-no-links': doc_no_links.strip(),
            'args': inspect.getargspec(obj)[0],
            'datanommer-hints': getattr(obj, 'hints', {}),
            'hints-invertible': getattr(obj, 'hinting_invertible', True),
            'hints-callable': getattr(obj, 'hinting_callable', None),
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


def validate_detail_value(ctx, value, config):
    if ctx.name == 'irc':
        if re.match(irc_regex, value) is None:
            raise ValueError("value must be a valid irc nick")
    elif ctx.name == 'email':
        mailserver = config['fmn.email.mailserver']
        return _validate_email(value, mailserver)
    elif ctx.name == 'android':
        if re.match(gcm_regex, value) is None:
            raise ValueError("not a valid android registration id")
    else:
        raise NotImplementedError("No validation scheme for %r" % ctx.name)
    # Happy.
    return

def _validate_email(value, mailserver):
    server = smtplib.SMTP(mailserver)
    code, reason = server.verify(value)
    if code < 300:
        return
    else:
        reason = reason.split(' ', 1)[-1]
        raise ValueError(reason)
