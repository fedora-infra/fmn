fmn.consumer
============

`fmn <https://github.com/fedora-infra/fmn>`_ is a family of systems to manage
end-user notifications triggered by
`fedmsg, the Fedora FEDerated MESsage bus <http://fedmsg.com>`_.

This module contains the backend worker daemon for Fedora Notifications.

There is a parental placeholder repo with some useful information you might
want to read through, like an `overview
<https://github.com/fedora-infra/fmn/#fedora-notifications>`_, a little
`architecture diagram <https://github.com/fedora-infra/fmn/#architecture>`_.


HACKING
-------

Find development instructions here: https://github.com/fedora-infra/fmn/#hacking

RUNNING
-------

There are three components to run in section of the project:

* the fedmsg consumer
* one or more workers
* the backend

The consumer is the part of the application that receives the messages from
fedmsg, it then sends them to the worker(s) who will see whose preferences
the message match (ie: to whom to send the notification and on which channel).
The worker(s) then send its results to the backend that receives them and
just do the IO: sending the email, posting to IRC and so on.


To run these parts, simply, start ``rabbitmq-server`` and ``redis`` and call,
in three different terminals (all running the same virtual-environment):

::

    $ fedmsg-hub
    $ python fmn/consumer/worker.py
    $ python fmn/consumer/backend.py


Handy Script
------------

There's a handy script in the ``scripts/`` dir for debugging why some user did
or did not receive a message.  It takes a username and a fedmsg msg_id and
tries to see if the two match up or not based on the production preferences for
that user.


Architecture
------------

::

                                                       +-------------+
                                                Read   |             |   Write
                                                +------+  prefs DB   +<------+
                                                |      |             |       |
     +                                          |      +-------------+       |
     |                                          |                            |   +------------------+   +--------+
     |                                          |                            |   |    |fmn.lib|     |   |        |
     |                                          v                            |   |    +-------+     |<--+  User  |
     |                                    +----------+                       +---+                  |   |        |
     |                                    |   fmn.lib|                           |  Central WebApp  |   +--------+
     |                                    |          |                           +------------------+
     |                             +----->|  Worker  +--------+
     |                             |      |          |        |
  fedmsg                           |      +----------+        |
     |                             |                          |
     |                             |      +----------+        |
     |   +------------------+      |      |   fmn.lib|        |       +--------------------+
     |   | fedmsg consumer  |      |      |          |        |       | Backend            |
     +-->|                  +------------>|  Worker  +--------------->|                    |
     |   |                  |      |      |          |        |       +-----+   +---+  +---+
     |   +------------------+      |      +----------+        |       |email|   |IRC|  |SSE|
     |                             |                          |       +--+--+---+-+-+--+-+-+
     |                             |      +----------+        |          |        |      |
     |                             |      |   fmn.lib|        |          |        |      |
     |                             |      |          |        |          |        |      |
     |                             +----->|  Worker  +--------+          |        |      |
     |                         RabbitMQ   |          |    RabbitMQ       |        |      |
     |                                    +----------+                   |        |      |
     |                                                                   v        v      v
     |
     |
     |
     v


FAQ
------------

Q: If the worker and backend complain about ::

    self.db[key] = value
    TypeError: String or Integer object expected for key, unicode found

A: Modify the config for `fedmsg.d/fmn.py` to use redis ::

    # Some configuration for the rule processors
    "fmn.rules.utils.use_pkgdb2": False,
    "fmn.rules.utils.pkgdb2_api_url": "http://209.132.184.188/api/",
    "fmn.rules.cache": {
        'backend': 'dogpile.cache.redis',
        'arguments': {
            'host': 'localhost',
            'port': 6379,
            'db': 0,
            'redis_expiration_time': 60*60*2,   # 2 hours
            'distributed_lock': True
        },
        # "backend": "dogpile.cache.dbm",
        # "expiration_time": 300,
        # "arguments": {
        #     "filename": "/var/tmp/fmn-cache.dbm",
        # },
    },

Q: When I run the worker and backend it constantly quits right away

A: Do you have `rabbitmq-server` and `redis` running? ::

    systemctl status rabbitmq-server redis

if not run ::

    systemctl start rabbitmq-server redis

Q: When running `fedmsg-hub` it shows that stuff are not initialized in the output

A: Have you updated the repo and ran the setup again? ::

    git pull
    workon fmn
    python setup.py develop

Q: I have `fedmsg-hub`, `worker.py` and `backend` running now what?

A: Load up the web interface and enable IRC and add your nick. Checkout `fmn.web <https://github.com/fedora-infra/fmn.web>`_  and `fmn <https://github.com/fedora-infra/fmn>`_ for more info.

Q: It's saying my nick is invalid

A: Is your nick registered? If not run this with the correct information ::

    /msg NickServ REGISTER password youremail@example.com

src: `freenode <https://freenode.net/kb/answer/registration>`_

Q: How do I know if it's working?

A: In IRC you should get contacted by `threebot` ::

    <threebot> <user>.id.fedoraproject.org has requested that notifications be sent to this nick
    <threebot> * To accept, visit this address:

Q: How do I stress test?

A: To be continued. Scripts are in process of being created
