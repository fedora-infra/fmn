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
