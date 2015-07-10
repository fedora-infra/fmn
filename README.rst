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

Handy Script
------------

There's a handy script in the ``scripts/`` dir for debugging why some user did
or did not receive a message.  It takes a username and a fedmsg msg_id and
tries to see if the two match up or not based on the production preferences for
that user.
