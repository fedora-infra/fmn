Fedora Notifications
====================

``fmn`` is a family of systems to manage end-user
notifications triggered by `fedmsg, the Fedora FEDerated MESsage bus
<http://fedmsg.com>`_.

The "wins" here are:

- A single place for email code to live, instead of being duplicated in
  every application that we write and deploy.  This will ostensibly reduce
  the amount of code we have to maintain.
- Diverse kinds of notifications.  Some users don't want email.
- A single place for end-users to manage notification preferences.
  Instead of having to tweak preferences in bodhi, koji, pkgdb, etc..
  they can choose what they do and don't want to receive at
  (hypothetically) https://apps.fedoraproject.org/notifications/

We would like to be able to serve notifications via these means,
listed in order by priority:

- Email.
- IRC private messages directed at users.
- Desktop popups.
- Android notifications via Google Cloud Messaging.
- Websocket notifications on webapps.
- User-specific RSS feeds

For terminology's sake, refer to these as the ``N`` notification ``contexts``.

Hacking
-------

- Clone the repo, cd into it.

- Set up a virtualenv:

  - ``$ mkvirtualenv fmn``

- The project is split into multiple sub packages, so run:

  - ``$ python setup-lib.py develop``
  - ``$ python setup-consumer.py develop``
  - ``$ python setup-web.py develop``

- Do the tests pass out of the box?

  - ``$ python setup-lib.py test``

- Create some dev data for the webapp:

  - ``$ python createdb.py --with-dev-data``

- Start the webapp:

  - ``$ python fmn/web/main.py``

- Edit the dev data to use your ``ircnick`` and email:

  - ``$ vim fedmsg.d/fmn.py``

- Run the consumer to give it a try:

  - ``$ fedmsg-hub``


Architecture
------------

::

    |                        +--------\
    |                   read |  prefs | write
    |                  +---->|  DB    |<--------+
    |                  |     \--------+         |
    |        +-----+---+---+            +---+---+---+---+   +----+
    |        |     |fmn.lib|            |   |fmn.lib|   |   |user|
    v        |     +-------+            |   +-------+   |   +--+-+
    fedmsg+->|consumer     |            |central webapp |<-----+
    +        +-----+  +---+|            +---------------+
    |        |email|  |irc||
    |        +-+---+--+-+-++
    |          |        |
    |          |        |
    v          v        v 

For each user, the central data store will keep ``N`` distinct profiles,
one for each notification ``context``.

Specification of a Profile
--------------------------

Here's a proposal:

A user's account has a series of messaging contexts.  A messaging context is
one of 'Email', 'IRC', 'Android', etc..

For each context, a user has an unlimited number of filters.

Each filter has an unlimited number of rules.

A rule is something like: "is a bodhi message" or "pertains to a package
owned by me." They will be implemented as python functions.  The database model
will refer to them in some form like ``fmn.rules:pertains_to_me`` or
``fmn.rules:is_a_bodhi_message``.  They can optionally take arguments, which
will be tricky.  For instance, ``fmn.rules:pertains_to_a_package_owned_by``
needs a username for it to make any sense.

::

  User ---+-------------------------+------------------+
          |                         |                  |
          V                         V                  V
         Email                     IRC               Android
          |                         |                  |
          +--->Filter1               +--->Filter1        +----->Filter1
          |       |                        |                    |
          |       +-> is a koji build      +-> pertains to a    +-> pertains
          |       |   completed message        package owned        to the
          |       |                            by me                package
          |       +-> pertains to a package                         'nethack'
          |       |   owned by me
          |       |
          |       +-> does not pertain to
          |           package 'nethack'
          |
          +--->Filter2
                  |
                  +-> is a bodhi message
                  |
                  +-> pertains to a package
                      owned by 'lmacken'

If *all* the rules match for *any* filter in a given context, a notification
is deployed for that context.  In other words, the filters are OR'd together
and the rules that make up a filter are AND'd together.  If multiple contexts
have a filter that succeeds, notifications are deployed for all of those
contexts.

Context-specific Delivery Metadata
----------------------------------

- context-specific delivery data?

  - For instance, my FAS username is ralph but
    my irc nick is threebean.  How will the irc daemon find that out?  Do we
    store it in the notif profile?  Or does the irc daemon query FAS?  If we
    store it in the notif profile, then it is public.  The data store is world
    readable.

  - The android notifications need a "device id" tied to each user.  Can this
    be public?

Future Features
---------------

Things that we would like to have, but don't necessarily need to be in a first
release can be listed here.

- Templates for new users.  Packagers should start with a "packager"
  profile for their email context.  You should be able to "clone" one of your
  context from one of a few existing templates.
