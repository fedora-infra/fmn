=========
Changelog
=========

v2.1.0
======

Features
--------

* Add support for ``git.repo.new`` messages from src.fedoraproject.org and
  migrate users of the old ``pkgdb.package.new`` message over to it
  (`#290 <https://github.com/fedora-infra/fmn/pull/290>`_).

* Remove upgradepath from the critical taskotron tasks as that check has
  been deprecated
  (`#269 <https://github.com/fedora-infra/fmn/pull/269>`_).

* Celery workers are now configured with the standard FMN logging config
  (`#267 <https://github.com/fedora-infra/fmn/pull/267>`_).

* Links shortened with da.gd now use HTTPS
  (`#274 <https://github.com/fedora-infra/fmn/pull/274>`_).

Bug fixes
---------

* Fix a bug where messages that mentioned a lot of packages created an
  email so large it couldn't be sent in a single email
  (`#273 <https://github.com/fedora-infra/fmn/pull/273>`_),

* Fix a bug where the database being unavailable caused FMN to crash
  (`#268 <https://github.com/fedora-infra/fmn/pull/268>`_),
  (`#271 <https://github.com/fedora-infra/fmn/pull/271>`_),
  (`#272 <https://github.com/fedora-infra/fmn/pull/272>`_).

* Restore summary in digest email when reporting verbose messages
  (`#278 <https://github.com/fedora-infra/fmn/pull/278>`_).

* X-Fedmsg-Username headers should not be duplicated
  (`#281 <https://github.com/fedora-infra/fmn/pull/281>`_).

* Set digest content limits to 1k messages and 500k content length
  (`#280 <https://github.com/fedora-infra/fmn/pull/280>`_).

* Add timestamp in single message emails
  (`#284 <https://github.com/fedora-infra/fmn/pull/287>`_).

* Limit single message emails to 500K characters to ensure multi-MB emails
  don't get stuck in the message queue
  (`#288 <https://github.com/fedora-infra/fmn/pull/288>`_).

Developer Improvements
----------------------

* Update the example Vagrantfile to Fedora 27
  (`#282 <https://github.com/fedora-infra/fmn/pull/282>`_).

Contributors
------------

This release contained code contributions from:

* Jeremy Cline
* Ricky Elrod
* Kamil Páral
* Patrick Uiterwijk
* Mattia Verga

Thank you! Many thanks to those who filed bug reports and feature suggestions,
as well.


v2.0.2
======

Bug fixes
---------

* Small performance improvements to the user to package mapping function
  (`#255 <https://github.com/fedora-infra/fmn/pull/255>`_).

* Change workers to run in pre-fork mode with concurrency 1
  (`#256 <https://github.com/fedora-infra/fmn/pull/256>`_).

* Handle batch messages in the delivery service without crashing
  (`#258 <https://github.com/fedora-infra/fmn/pull/258>`_).

* Refactor the message formatting functions so they don't crash on unformattable
  messages (`#259 <https://github.com/fedora-infra/fmn/pull/259>`_).

* Encode email with UTF-8 before sending
  (`#260 <https://github.com/fedora-infra/fmn/pull/260>`_).

* Ignore forks when determining what packages a user maintains
  (`#264 <https://github.com/fedora-infra/fmn/pull/264>`_).

* Disable or fix email addresses that can't be delivered to anymore
  (`#265 <https://github.com/fedora-infra/fmn/pull/265>`_).


v2.0.1
======

Bug fixes
---------

* Fix a caching issue where disabling delivery methods wouldn't be picked up
  by all worker processes (`#251 <https://github.com/fedora-infra/fmn/issues/251>`_).

* Fix the path in the distributed systemd unit file for the delivery service:
  it is now /usr/share/fmn/ rather than /usr/lib/share/
  (`#246 <https://github.com/fedora-infra/fmn/pull/246>`_).

* Fix a bug in the package ownership queries that caused all rules querying for
  package watchers to be ignored
  (`#248 <https://github.com/fedora-infra/fmn/pull/248>`_).


2.0.0
=====

Backwards-incompatible Changes
------------------------------

The default queue names for FMN have changed. Messages that need to be processed
for recipients are placed in the ``fmn.tasks.unprocessed_messages`` queue and
messages ready for delivery are in the ``fmn.backends.<backend_name>`` queues.


Features
--------

* The FMN workers and backend is now implemented using Celery
  (`#231 <https://github.com/fedora-infra/fmn/pull/231>`_,
  `#232 <https://github.com/fedora-infra/fmn/pull/232>`_,
  `#234 <https://github.com/fedora-infra/fmn/pull/234>`_,
  `#235 <https://github.com/fedora-infra/fmn/pull/235>`_,
  `#237 <https://github.com/fedora-infra/fmn/pull/237>`_,
  `#238 <https://github.com/fedora-infra/fmn/pull/238>`_,
  `#241 <https://github.com/fedora-infra/fmn/pull/241>`_,)

* Rules for Greenwave
  (`#244 <https://github.com/fedora-infra/fmn/pull/244>`_)

* Configuration defaults are now provided
  (`#239 <https://github.com/fedora-infra/fmn/pull/239>`_)


1.5.0
=====

Features
--------

* The IRC client can now connect via TLS and authenticate with NickServ
  (`#228 <https://github.com/fedora-infra/fmn/pull/228>`_).

* Handle generic exceptions in backends by requeuing the message
  (`#229 <https://github.com/fedora-infra/fmn/pull/229>`_).


1.4.1
=====

Bug fixes
---------

* Ensure the new CI rules appear in the filter list (`#224
  <https://github.com/fedora-infra/fmn/pull/224>`_).

* Migrate the default user filters to ignore successful CI steps
  (`#225 <https://github.com/fedora-infra/fmn/pull/225>`_)


1.4.0
=====


Features
--------

* The bootstrap CSS theme is now configurable using the 'fmn.web.theme_css_url'
  configuration key (`#202 <https://github.com/fedora-infra/fmn/pull/202>`_).

* FMN can now be configured to query Pagure rather than PkgDB
  using the "fmn.rules.utils.pagure_api_url" and "fmn.rules.utils.use_pagure_for_ownership"
  configuration flags (`#206 <https://github.com/fedora-infra/fmn/pull/206>`_).

* FMN can now be configured to subscribe to certain topics rather than everything
  using the 'fmn.topics' configuration field
  (`#218 <https://github.com/fedora-infra/fmn/pull/218>`_).

* Initial rules for CI-related messages have been added
  (`#221 <https://github.com/fedora-infra/fmn/pull/221>`_).


Bugfixes
--------

* Fix the CSRF errors for libravatar.org
  (`#214 <https://github.com/fedora-infra/fmn/pull/214>`_).

* Fix an issue where example messages were never shown for new filters
  (`#220 <https://github.com/fedora-infra/fmn/pull/220>`_).


Development Improvements
------------------------

* The Vagrant environment now includes datanommer
  (`#211 <https://github.com/fedora-infra/fmn/pull/211>`_).


Many thanks to the following contributors for their work on this release:

* Ralph Bean
* Pierre-Yves Chibon
* Jeremy Cline
* Francois Marier
* Matt Prahl


1.3.1
=====

Bugfixes
--------

* Fixes compatibility with old versions of dogpile.cache (less than 0.6.3) by
  backporting the function being used. This backport is available under the
  BSD license.


1.3.0
=====

Refactors
---------

* Merge the fmn.sse repository into the fmn repository.

* Merge the fmn.web repository into the fmn repository.

Rule Changes
------------

* Taskotron rules: Particular tasks can now be matched using wildcards (PR #197).

* Taskotron rules: add abicheck as a critical task (PR #198).

Performance Improvements
------------------------

* Loading rules is now cached in memory which speeds up user creation by several
  orders of magnitude: creating 100 users went from 221 seconds to 3.3
  (Issue #191).

* The map of rule strings to rule Python objects is now cached which improves
  preference loading time by approximately an order of magnitude.

Bugfixes
--------

* Fix a bug where cache regions were configured to never expire cached keys
  (Issue #194).


1.2.1
=====

1.2.1 is a bug fix release.

Bugfixes
--------

* Stop trying to shuffle preferences in the worker consumer (#181)


1.2.0
=====

Features
--------

* Emails now contain headers to indicate to clients that they are auto-
  generated. This should stop them from auto-responding (#165).

* New rules for the Module Build Service (#174).

Bugfixes
--------

* Be fault-tolerant towards missing 'owner' field in copr msgs (commit d46464e06).

* Messages that can't be sent are now requeued (#169).

* Update to the generic rule for packages to account for namespaces in pkgdb2 (#177).


1.1.0
=====

* Introduce an fmn-createdb script


1.0.0
=====

* Documentation is now available `online <https://fmn.readthedocs.io/>`_.

* Merge the fmn.lib, fmn.consumer, and fmn.rules repositories. The changelogs
  for those projects since the last release of each is included below.
  - https://github.com/fedora-infra/fmn.lib/
  - https://github.com/fedora-infra/fmn.rules/

* The FMN consumer now requeues messages it failed to send with the IRC backend
  (https://github.com/fedora-infra/fmn.consumer/pull/96).

* There is now a Server-Sent Events backend for the FMN consumer
  (https://github.com/fedora-infra/fmn.consumer/pull/92 and
  https://github.com/fedora-infra/fmn.lib/pull/62).

* Emails are now split up into 20MB chunks if necessary
  (https://github.com/fedora-infra/fmn.consumer/pull/88).

* The digest producer is now run in a separate process
  (https://github.com/fedora-infra/fmn.consumer/pull/86).

* The API for ``handle_batch`` in the consumer has changed to accept a list
  of message dictionaries rather than ``QueuedMessage`` objects
  (https://github.com/fedora-infra/fmn.consumer/pull/86)
