Fedora Notifications
====================

Fedora Notifications is a family of systems built to manage end-user
notifications triggered by `fedmsg <http://fedmsg.com>`_, the fedora FEDerated
MeSsaGe bus.

The wins here are:

- Diverse kinds of notification media: Some users don't want email. At present
  we can do notifications over email and IRC privmsg. In the future we hope to
  add Android push notifications, desktop popups, and websocket integration
  across all of our apps.
- A single place for end-users to manage notification preferences: As it stands
  right now, you have to update notification preferences (if you can do so at
  all) in many different apps in many different places. (bodhi, koji, pkgdb,
  etc..). With this app (Fedora Notifications), you can choose what you do and
  don't want to receive in one place -- right here.
- A single place for email code to live -- instead of being duplicated in every
  application that we write and deploy. This will ostensibly reduce the amount
  of code that the infrastructure team has to maintain.

----

In a nutshell, here's the way this application works:

- You login and set up some preferences here, in this webapp.
- Events occur in Fedora Infrastructure and are broadcast over fedmsg.
- This application receives those events and compares them against your
  preferences. If there's a match, then it forwards you a notification.

We maintain a `lot of applications <https://apps.fedoraproject.org>`_. Over
time, there has been an initiative to get them all speaking a similar language
on the backend with fedmsg. Take a look at the `list of fedmsg topics
<http://fedmsg.com/en/latest/topics/>`_ to see what all is covered.

Some Terminology
================

Rule
----

This is smallest, most atomic object in the Fedora Notifications system. It is
a simple rule that can be applied to a fedmsg message. It can evaluate to
``True`` or ``False``.

It has a name and a description. Some examples of rules are:

- "is a *bodhi* message"
- "is a *wiki edit* message"
- "relates to the user *lmacken*"
- "relates to the package *nethack*"
- "relates to a package *owned by me in pkgdb*"

We have a long list of rules defined. You'll see them when you go to set up
your first filter

Filter
------

To craft your preferences, you will build filters out of rules. Filters have a
name (that you give them). An example could be something like:

- My bodhi packager filter

  - "is a bodhi message"
  - "relates to a package that I own"

You will receive notifications for this filter *if and only if* a given message
**both** is a bodhi message and is about a package owned by you.

----

Note that, if you wanted to get notifications about bodhi updates created by
multiple users, you would need to create distinct filters for each one.

- My bodhi lmacken filter

  - "is a bodhi message"
  - "relates to the user **lmacken**"

- My bodhi toshio filter

  - "is a bodhi message"
  - "relates to the user **toshio**"

You could not combine those both into the same filter, because *all rules on a
filter* must evalulate to ``True`` for the filter to trigger a notification.

Messaging Context
-----------------

This is the medium over which we'll send a message. You can have one set of
preferences for an email messaging context, and another set of preferences for
an irc messaging context.

When a fedmsg message arrives in the system, if *any one filter* on one of your
messaging contexts evaluates to ``True``, then you will receive a notification
for that context. If some filters evaluate to ``True`` for multiple contexts,
you will receive notifications for all those contexts.

Dénouement
==========

You can report `issues
<https://github.com/fedora-infra/fmn/issues>`_ and find the
`source <https://github.com/fedora-infra/fmn/>`_ on github.
The development team hangs out in ``#fedora-apps``. Please do stop by and say
hello.
