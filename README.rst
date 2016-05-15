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


To run these parts, simply call, in three different terminals:

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
