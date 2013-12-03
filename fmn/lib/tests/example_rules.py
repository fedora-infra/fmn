""" Some example rules for the test suite. """


def wat_rule(config, message):
    return message['wat'] == 'blah'


def not_wat_rule(config, message):
    return message['wat'] != 'blah'
