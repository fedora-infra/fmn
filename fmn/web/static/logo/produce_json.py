import requests
import hashlib
import random
import json

import fedmsg.config
import fedmsg.meta
config = fedmsg.config.load_config()
fedmsg.meta.make_processors(**config)

N_OUTPUT = 15
N_INPUT = 13
N_USERS = 12

response = requests.get("https://badges.fedoraproject.org/leaderboard/json")
d = response.json()

usernames = [entry['nickname'] for entry in d['leaderboard']]

def libravatar(username):
    template = "http://cdn.libravatar.org/avatar/{value}?s=16"
    openid = "http://%s.id.fedoraproject.org/" % username
    value = hashlib.sha256(openid).hexdigest()
    return template.format(value=value)


# TODO these need icons
contexts = [
    {
        'name': ctx,
        'group': 1,
        'icon': icon,
    } for ctx, icon in [
        ('Email', 'icon-envelope.png'),
        ('IRC', 'icon-user.png'),
        ('Android', 'icon-phone.png'),
        ('Desktop', 'icon-desktop.png'),
        ('Websockets', 'icon-websockets.png'),
    ]
]

no_avatar = ['ausil', 'patches', 'nb', 'kalev']
users = [
    {
        'name': username,
        'group': 2,
        'icon': libravatar(username),
    } for username in usernames if username not in no_avatar]


sources = [
    {
        'name': proc.__obj__,
        'icon': proc.__icon__,
        'group': 3,
    } for proc in fedmsg.meta.processors]

# TODO -- keep track of these to get more icons down the road.
# Clean out bogus ones.
for i in range(len(sources)):
    if sources[i]['icon'] is None:
        del sources[i]['icon']

# Furthermore
for i in reversed(range(len(sources))):
    if 'icon' not in sources[i]:
        sources.pop(i)

#sources = random.sample(sources, 10)
users = random.sample(users, N_USERS)

nodes = contexts + users + sources


def make_random_links_1(N):
    context_indices = range(len(contexts))
    user_indices = range(len(contexts), len(contexts) + len(users))
    random.shuffle(context_indices)
    random.shuffle(user_indices)
    for i in range(N):
        yield {
            'source': context_indices[i % len(context_indices)],
            'target': user_indices[i % len(user_indices)],
            'type': 'output',
        }

def make_random_links_2(N):
    context_indices = range(len(contexts))
    source_indices = range(len(contexts) + len(users),
                    len(contexts) + len(users) + len(sources))
    random.shuffle(context_indices)
    random.shuffle(source_indices)
    for i in range(N):
        yield {
            'source': source_indices[i % len(source_indices)],
            'target': context_indices[i % len(context_indices)],
            'type': 'input',
        }

links = list(make_random_links_1(N_OUTPUT)) +\
        list(make_random_links_2(N_INPUT))

print json.dumps(dict(nodes=nodes, links=links), indent=2)
