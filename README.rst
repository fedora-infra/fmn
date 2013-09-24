fedmsg-notifications
====================

``fedmsg-notifications`` is a family of systems to manage end-user
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

- Do the tests pass out of the box?

  - ``$ python setup-lib.py test``

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

A user's profile consists of a series of whitelists for a series of contexts.

For a single ``context``, the profile looks something like a `datagrepper
<https://apps.fedoraproject.org/datagrepper/>`_ query (it looks *kind* of like
conjunctive normal form):

- If nothing is specified, all messages get through.
- If any category is specified, all messages get through for that category and
  no others.
- If multiple categories are specified, all messages get through if the
  message is in *any* of those categories.
- Same goes for "topics" as for "categories".
- If a user (or multiple users) are specified, messages that match *any* of
  those users and *also* match any argued categories are allowed through.
- If a package (or multiple packages) are specified, messages that match *any*
  of those packages and *also* match any other argued parameter types are
  allowed through.

The `datagrepper <https://apps.fedoraproject.org/datagrepper/>`_ docs explain
it a bit better than here.

The above schema is probably insufficient to cover all our scenarios.  Let's
try brainstorming some, see what we need, then come up with something that
meets those needs.

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
