fedmsg-notifications
====================

``fedmsg-notifications`` is a family of systems to manage end-user
notifications triggered by the `fedmsg, the Fedora FEDerated MESsage bus
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

Architecture
------------

There are multiple daemons, arranged in a hub-and-spoke model.

The center of the system is a "passive" data store web application.
It holds on to notification profiles for users for a number of
different contexts.  Users can manage their preferences via HTML
forms served by this webapp, or by interacting with client programs
(on gnome-shell, android, etc..) that communicate with the central
webapp's JSON API.

For each user, the central data store will keep ``N`` distinct profiles,
one for each notification ``context``.

Elsewhere, we will keep running ``N`` daemons, also one for each
notification ``context``.  Each one is independently responsible for
monitoring the fedmsg bus.  When a new message is received, each will
ask the central data store "for this message, what users should receive it
for *my* context?"  Each daemon will then deliver the notification to each
of the expectant users via the context for which it is responsible.

For example:  A message is published that a new build of nethack has been
completed.  The email daemon, the irc daemon, the android daemon, and the rss
daemon all receive it.  They each ask the store the question.  The email
daemon then sends a notification email to lmacken and ralph, the irc daemon
pings lmacken and abadger1999, the android daemon tells GCM to notify relrod,
and the rss daemon rebuilds nirik's rss feed to include the new item.

Special Case
------------

The desktop notification tool is a special case.

The webapp notification preferences are a special case.

TODO -- elaborate on why this is the case and how to solve it

Specification of a Profile
--------------------------

TODO -- elaborate on what is in a profile.

- Filtering information like we have elsewhere now
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
