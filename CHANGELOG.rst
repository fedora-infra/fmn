=========
Changelog
=========

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
