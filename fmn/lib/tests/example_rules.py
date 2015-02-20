""" Some example rules for the test suite. """

import fmn.lib.hinting


def wat_rule(config, message):
    return message['wat'] == 'blah'


def not_wat_rule(config, message):
    return message['wat'] != 'blah'


@fmn.lib.hinting.hint(categories=['whatever'])
def hint_masked_rule(config, message, argument1):
    """ This is a docstring.

    For real, it is a docstring.
    """
    return True


def _func(config, argument1):
    return {'the-hint-is': [argument1]}


@fmn.lib.hinting.hint(callable=_func)
def callable_hint_masked_rule(config, message, argument1):
    return True
