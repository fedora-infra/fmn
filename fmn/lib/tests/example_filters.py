""" Some example filters for the test suite. """


def wat_filter(config, message):
    return message['wat'] == 'blah'


def not_wat_filter(config, message):
    return message['wat'] != 'blah'
