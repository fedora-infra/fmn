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

The desktop notification tool and the webapp notification widget are special
cases.

The other daemons (irc, email, rss) run as a single instances each serving
*all* users.  The desktop tool and the webapp widget run as many instances,
one instance per user (each user so-opting will have an instance of the
desktop notifier running on their system; each user with the webapp widget
enabled will have it running in their browser as they visit fedoraproject.org
pages).  For terminology's sake, we'll call the former `one-to-many contexts`
(one process serves many users);  the desktop notifier and the webapp widget
are `one-to-one contexts` (one process serves one user).

Above, we stated that the daemon(s) for each context "ask a question" of the
central data store for each message they receive.  For the `one-to-many
context` daemons, this is no big deal.  If there are 4 different such
contexts, 4 JSON requests will be made of the central data store.  We can
handle that.  For the `one-to-one context` processes, however, load is going
to scale up quickly.  If we have 1000 simultaneous users of the desktop
notification tool, for each new message that comes across fedmsg they will all
simultaneously make the exact same query on the central datastore: "who should
get this message for my context?"

We can do some aggressive caching to mitigate this, but if we find that it is
unacceptable, we can write libs so that the `one-to-one context` processes can
perform decision-making for themselves.  They could ask the central data store
to *export* the raw preferences for their context and, using that information,
decide whether each new incoming message should be displayed or discarded.
The fedmsg-notify-daemon does this already (it was the first of its kind).
While it is nice to reduce load on the central data store, we have to
duplicate the rule-processing logic kept there.  If we write it once in
python, do we have to maintain a fork in javascript for webapps to use?
Hopefully not.  Hopefully caching will obviate this.

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
