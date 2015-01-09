""" Helpers for "datanommer hints" for rules.

Rules can optionally define a "hint" for a datanommer query.  For
instance, if a rule has to do with filtering for bodhi messages, then a
provided hint could be {'category': 'bodhi'}.  This simply speeds up the
process of looking for potential message matches in the history by
letting the database server do some of the work for us.  Without this, we
have to comb through literally every message ever and then try to see
what matches and what doesn't in python-land:  Slow!

Rules define their hints with the @hint decorator defined here.

When querying datanommer, the ``gather_hinting`` helper here can be used to
construct the hint dict for ``datanommer.grep(..., **hints)``.
"""

import collections
import functools

import fedmsg.config


def hint(invertible=True, **hints):
    """ A decorator that can optionally hang datanommer hints on a rule. """
    def wrapper(fn):
        @functools.wraps(fn)
        def replacement(*args, **kwargs):
            return fn(*args, **kwargs)

        # Hang hints on the function.
        replacement.hints = hints
        replacement.hinting_invertible = invertible
        return replacement

    return wrapper


def prefixed(topic, prefix='org.fedoraproject'):
    config = fedmsg.config.load_config()  # This is memoized for us.
    return '.'.join([prefix, config['environment'], topic])


def gather_hinting(filter, valid_paths):
    """ Construct hint arguments for datanommer from a filter. """

    hinting = collections.defaultdict(list)
    for rule in filter.rules:
        root, name = rule.code_path.split(':', 1)
        info = valid_paths[root][name]
        for key, value in info['datanommer-hints'].items():

            # If the rule is inverted, but the hint is not invertible, then
            # there is no hinting we can provide.  Carry on.
            if rule.negated and not info['hints-invertible']:
                continue

            # Otherwise, construct the inverse hint if necessary
            if rule.negated:
                key = 'not_' + key

            # And tack it on.
            hinting[key] += value

    return hinting
