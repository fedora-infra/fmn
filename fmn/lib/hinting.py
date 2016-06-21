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

import fedmsg.config

import logging
log = logging.getLogger('fmn.lib.hinting')


def hint(invertible=True, callable=None, **hints):
    """ A decorator that can optionally hang datanommer hints on a rule. """

    def wrapper(fn):
        # Hang hints on fn.
        fn.hints = hints
        fn.hinting_invertible = invertible
        fn.hinting_callable = callable
        return fn

    return wrapper


def prefixed(topic, prefix='org.fedoraproject'):
    config = fedmsg.config.load_config()  # This is memoized for us.
    return '.'.join([prefix, config['environment'], topic])


def gather_hinting(config, rules, valid_paths):
    """ Construct hint arguments for datanommer from a list of rules. """


    hinting = collections.defaultdict(list)
    for rule in rules:
        root, name = rule.code_path.split(':', 1)
        info = valid_paths[root][name]

        if info['hints-callable']:
            # Call the callable hint to get its values
            result = info['hints-callable'](config=config, **rule.arguments)

            # If the rule is inverted, but the hint is not invertible, then
            # there is no hinting we can provide.  Carry on.
            if rule.negated and not info['hints-invertible']:
                continue

            for key, values in result.items():
                # Negate the hint if necessary
                key = 'not_' + key if rule.negated else key
                hinting[key].extend(values)

        # Then, finish off with all the other ordinary, non-callable hints
        for key, value in info['datanommer-hints'].items():

            # If the rule is inverted, but the hint is not invertible, then
            # there is no hinting we can provide.  Carry on.
            if rule.negated and not info['hints-invertible']:
                continue

            # Otherwise, construct the inverse hint if necessary
            key = 'not_' + key if rule.negated else key

            # And tack it on.
            hinting[key] += value

    log.debug('gathered hinting %r', hinting)
    return hinting
