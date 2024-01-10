<!--
SPDX-FileCopyrightText: Contributors to the Fedora Project

SPDX-License-Identifier: MIT
-->

# Rolling a Release

## Releasing on PyPI

This documents how a release is made.

Unless otherwise noted, files are referenced relative to and commands should be executed from the
top-level directory of the repository.

### Bump the Version

Use `poetry version (patch|minor|major|…)` to bump the version in `pyproject.toml`, e.g.:

```
$ poetry version patch
```

Depending on the nature of changes in the release, choose an appropriate “bump rule” (see `poetry
version --help` for details).

Run `poetry install --all-extras` to recreate the metadata files.

### Generate Changelog

We want to document what changes between releases. To do that, we use `towncrier` which collates
changelog snippets and adds them to `docs/changelog.md`:

```
$ poetry run towncrier build
Loading template...
Finding news fragments...
Rendering news fragments...
Writing to newsfile...
Staging newsfile...
Removing news fragments...
I want to remove the following files:
…
Is it okay if I remove those files? [Y/n]: y
Done!
```

Review the changes to `docs/changelog.md`, e.g. using `git diff`.

Afterwards, commit the changes to git. The commit should contain the extended `docs/changelog.md`
file as well as the snippet files which were removed in the previous step.

Commit the changes to git.

### Tag the Release

Tag this commit with a GPG-signed tag using the plain version number, e.g.:

```
$ git tag --sign 3.0.0
```

Push both the `develop` branch and the tag you just created to the GitHub repository:

```
$ git push origin develop 3.0.0
```

### Build the Artifacts

Build the source tarball and installable Python wheel archive:

```
$ poetry build
```

Th resulting archives will be placed into the `dist/` directory.

### Create a Release on GitHub

Open [`https://github.com/fedora-infra/fmn/tags`](https://github.com/fedora-infra/fmn/tags) in a web
browser, navigate to the just created tag (it should be at the top) and select `Create release` from
the “meatballs” menu to its right.

In the page that opens add a title like `Release 3.0.0` and fill in (high-level) details about the
release in the text area below. Beneath it, there is an area labelled `Attach binaries by dropping
them here or selecting them.` Add the previously built source tarball (e.g. `fmn-3.0.0.tar.gz`) to
the release, either by clicking in that area, navigating to the `dist/` directory and selecting the
tarball, or by dragging and dropping it from a file manager into the same area.

Click the button labelled `Publish release`.

### Publish Python Package to PyPI

To publish the Python package to the [Python Package Index](https://pypi.org), you need to be a
maintainer of the [`fmn` package](https://pypi.org/project/fmn/) there and have a PyPI API token
created for your account and configured in
[`~/.pypirc`](https://packaging.python.org/en/latest/specifications/pypirc/#using-a-pypi-token).

Then you can publish the source tarball and wheel of the release using Poetry like this:

```
$ poetry publish
```

### Congratulations!

You’re done! 🥳

## Deploying to Fedora Infrastructure

FMN is deployed through Openshift, which tracks the `staging` and `stable` branches for the staging
and production environments respectively.

### Staging

When the code in the `develop` branch is suitable for testing in the staging environment, merge it
in the staging branch and push it to the repository:

```
$ git co staging
$ git merge --ff-only develop
$ git push
```

Do not create a pull request and merge it, as [Github does not support fast-forward
merges](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github#rebasing-and-merging-your-commits),
it will create a new commit SHA and the commit will appear different from the `develop` branch.

This will trigger a build in OpenShift in the staging environment. Make sure the new version is
actually deployed by looking at the footer of the FMN page.

### Production

When the code in the `staging` branch has been sufficiently tested and that a window is open for a
production deployment, merge it into the stable branch and push it to the repository:

```
$ git co stable
$ git merge --ff-only staging
$ git push
```

Again, do not create a PR, you need to use the command line and the `--ff-only` option.

This will trigger a build in OpenShift in the production environment. Make sure the new version is
actually deployed by looking at the footer of the FMN page.

It is advised to roll a release on PyPI with the content of the `stable` branch (and therefore the
code that is deployed in production).
