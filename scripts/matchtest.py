""" Script to test if a user will get a given message.

Requires:
- python-munch
- python-requests
- python-click
- python-fmn-lib
- python-fmn-rules
- python-fedmsg-meta-fedora-infrastructure

"""
from __future__ import print_function

import munch
import requests
import click

import fmn.lib

import fedmsg.config
import fedmsg.meta
import fedmsg.utils

import logging.config


config = fedmsg.config.load_config()
logging.config.dictConfig(config.get('logging', {'version': 1}))

valid_paths = fmn.lib.load_rules(root='fmn.rules')
fedmsg.meta.make_processors(**config)


def get_preference(username, context):
    url = 'https://apps.fedoraproject.org/notifications/api/' + \
        '%s.id.fedoraproject.org/%s/' % (username, context)
    preference = requests.get(url).json()
    preference = rehydrate_preference(preference)
    return preference


def get_message(msg_id):
    url = 'https://apps.fedoraproject.org/datagrepper/id?id=%s' % msg_id
    return requests.get(url).json()


def rehydrate_preference(preference):
    for fltr in preference['filters']:
        fltr['rules'] = [munch.Munch(r) for r in fltr['rules']]
        for rule in fltr['rules']:
            code_path = str(rule.code_path)
            rule.fn = fedmsg.utils.load_class(code_path)

    return preference


@click.command()
@click.option('--context', default="email", help="fmn delivery context")
@click.argument('username')
@click.argument('msg_id')
def main(context, username, msg_id):
    preferences = [get_preference(username, context)]
    message = get_message(msg_id)
    subtitle = fedmsg.meta.msg2subtitle(message, **config)

    matches = fmn.lib.recipients(preferences, message, valid_paths, config)

    print("-" * 60)
    print(len(matches), "matches for", subtitle)
    print(matches)


if __name__ == '__main__':
    main()
