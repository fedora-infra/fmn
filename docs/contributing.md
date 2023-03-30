<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

# Contributor Guide

You need to be legally allowed to submit any contribution to this project. What this means in detail
is laid out at the [Developer Certificate of Origin](https://developercertificate.org) website.
The mechanism by which you certify this is adding a `Signed-off-by` trailer to git commit log
messages, you can do this by using the `--signoff/-s` option to `git commit`.

## Changelog

Significant changes should appear in the [ChangeLog](changelog). To that end, contributors must
create a changelog entry using [Towncrier](https://towncrier.readthedocs.io/) and the appropriate
category.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

The syntax to create a changelog entry is the following:

```
poetry run towncrier create -c "Added a cool feature" issuenumber.category.md
```

Where `issuenumber` is the issue number in Github, and `category` is one of:

- `security` in case of vulnerabilities
- `removed` for now removed features
- `deprecated` for soon-to-be removed features
- `added` for new features
- `changed` for changes to existing functionality
- `fixed` for any bug fixes

For example:

```
poetry run towncrier create -c "Added a cool feature!" 42.added.md
```

If the change does not fit into any category, prefix the filename with a "plus", for example:

```
poetry run towncrier create -c "A fix without an issue number!" +something-unique.fixed.md
```
