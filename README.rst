FedMSG Notifications
====================

``fmn`` is a family of systems to manage end-user notifications triggered by
`fedmsg, the FEDerated MESsage bus <http://fedmsg.com>`_. ``fmn`` provides a
single place for all applications using ``fedmsg`` to notify users of events.
Notifications can be delivered by email, irc, and server-sent events. Users
can configure their notifications for all the applications they use in one
place.

FMN is deployed in `Fedora <https://apps.fedoraproject.org/notifications/>`_.


Documentation
-------------

Documentation is available in the docs/ directory. It is easiest to build them
in the Vagrant environment::

    $ vagrant ssh
    $ workon python3-fmn
    $ cd devel/docs
    $ make html

You need sphinx, sqlalchemy_schemadisplay, and graphviz to build the
documentation.


Contributing
------------

Consult the contribution guide in our documentation!
