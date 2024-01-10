<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This project uses [*towncrier*](https://towncrier.readthedocs.io/) and the changes for the upcoming release can be found in <https://github.com/fedora-infra/fmn/tree/main/changelog.d/>.

<!-- towncrier release notes start -->

## [3.3.0](https://github.com/fedora-infra/fmn/tree/3.3.0) - 2024-01-10


### Added

- Add a footer to email notifications with a link to the rule that generated it [#895](https://github.com/fedora-infra/fmn/issues/895)


### Changed

- Remove the refence to the old FMN on the home page


### Fixed

- Explain where the destinations come from [#892](https://github.com/fedora-infra/fmn/issues/892)
- Adjust to backwards-incompatible changes in aiosmtplib 3.x
- Prevent selecting a destination from closing the modal

## [3.2.0](https://github.com/fedora-infra/fmn/tree/3.2.0) - 2023-09-21

### Added

- Send the cache building stats to collectd [#913](https://github.com/fedora-infra/fmn/issues/913)

### Fixed

- Disable a user's rules when the user is disabled. This will happen only after the FASJSON cache
  expires, so there will be a delay. Disabled rules will not be re-enabled if the user is re-enabled. [#826](https://github.com/fedora-infra/fmn/issues/826)
- Add a Cancel button when creating a rule and a link back to the rules list in the user dropdown [#877](https://github.com/fedora-infra/fmn/issues/877)
- Allow address extentions (``+``) in email addresses [#912](https://github.com/fedora-infra/fmn/issues/912)
- Don't crash when we timeout reaching the Matrix server [#971](https://github.com/fedora-infra/fmn/issues/971)
- Fix the creation of the "My Events" tracking rule [#984](https://github.com/fedora-infra/fmn/issues/984)


## [3.1.0](https://github.com/fedora-infra/fmn/tree/3.1.0) - 2023-08-09

### Removed

- Get rid of our support for synchronous DB [#870](https://github.com/fedora-infra/fmn/issues/870)

### Added

- Store how long rebuilding the cache took.
  Add a CLI to delete cache locks before they expire. [#869](https://github.com/fedora-infra/fmn/issues/869)
- Add a way to extend the email notification's body with, for example, a git patch [#916](https://github.com/fedora-infra/fmn/issues/916)

### Changed

- Use the new asyncio support in `sqlalchemy_helpers` [#PR933](https://github.com/fedora-infra/fmn/issues/PR933)
- Adjust to recent changes in tinystage [#PR933](https://github.com/fedora-infra/fmn/issues/PR933)
- Rebuild the cache instead of deleting it when a cache-invalidating message arrives [#869](https://github.com/fedora-infra/fmn/issues/869)

### Fixed

- Frontend: handle errors when querying destinations [#878](https://github.com/fedora-infra/fmn/issues/878)
- API: Allow rule names to be None in the outgoing Fedora messages.
  Message schema: make rule.id and user.name required as well. [#879](https://github.com/fedora-infra/fmn/issues/879)
- IRC sender: handle libera.chat not sending us the `LOGGED_IN` response [#884](https://github.com/fedora-infra/fmn/issues/884)
- Email sender: close the connection before reconnecting [#885](https://github.com/fedora-infra/fmn/issues/885)
- Handle Ipsilon error on login [#890](https://github.com/fedora-infra/fmn/issues/890)
- Avoid causing transaction serialization failures in the cache by making those transactions read-only [#922](https://github.com/fedora-infra/fmn/issues/922)



## [3.0.0](https://github.com/fedora-infra/fmn/tree/3.0.0) - 2023-04-14

### Changed

- Complete rewrite of FMN
