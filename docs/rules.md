<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

# Rules

*Rules* in FMN consist of several components: One [*Tracking Rule*](#tracking-rules), and
potentially many [*Filters*](#filters) and [*Destinations*](#destinations) (grouped into
[*Generation Rules*](#generation-rules)). The *Message Consumer* looks at all messages transported
over the bus and if any match a *Rule*, *Notifications* will be sent to the respective *Notification
Sender*, one instance of each is responsible for actually sending out emails and chat messages over
IRC or Matrix, respectively.

## Tracking Rules

Each *Rule* has exactly one *Tracking Rule* which specifies what messages should be tracked, e.g.
messages that concern:

* Artifacts owned by the user or a group the user is member of,
* specific named artifacts,
* the user themselves, or
* followed users.

If a *Tracking Rule* matches, its [*Generation Rules*](#generation-rules) will be consulted for
further processing.

## Generation Rules

Each *Rule* contains one or more *Generation Rules* which group together zero or more
[*Filters*](#filters) and one or more [*Destinations*](#destinations). If no [*Filters*](#filters)
exist, or all of them match, *Notifications* will be created for each [*Destination*](#destinations)
which are processed by the respective *Sender*.

This lets users e.g. specify that messages of a lower severity should be sent via email, while
higher severities should let FMN ping the user via IRC or Matrix.

## Filters

*Filters* further restrict if a message should be matched by a *Rule* and notifications should be
sent. Users can configure filters for these criteria:

* The name of the application sending a message.
* The severity(\*) of the message.
* If a message was caused by an action of the user.
* If the message topic matches a certain glob pattern.

(\*): At this point, we don’t know that any app in Fedora infrastructure tags its messages with a
severity, which makes them default to `INFO`.

## Destinations

A *Destination* contains information about how a user should be notified if a *Rule* matches, e.g.
via email, IRC or Matrix. The destinations available to a user are retrieved from their account and
can be configured in [*Noggin*](https://accounts.fedoraproject.org).
