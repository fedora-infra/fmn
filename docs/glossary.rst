Glossary
========

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

.. note::
    if you wanted to get notifications about bodhi updates created by
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
^^^^^^^^^^^^^^^^^

This is the medium over which we'll send a message. You can have one set of
preferences for an email messaging context, and another set of preferences for
an irc messaging context.

When a fedmsg message arrives in the system, if *any one filter* on one of your
messaging contexts evaluates to ``True``, then you will receive a notification
for that context. If some filters evaluate to ``True`` for multiple contexts,
you will receive notifications for all those contexts.
