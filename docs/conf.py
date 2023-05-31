# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

topdir = os.path.abspath("../")
sys.path.insert(0, topdir)

import fmn.core.version  # NOQA


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "FMN"
copyright = "2023, Fedora Infrastructure"
author = "Fedora Infrastructure"

# The short X.Y version
version = ".".join(fmn.core.version.__version__.split(".")[:2])

# The full version, including alpha/beta/rc tags
release = fmn.core.version.__version__


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "github_user": "fedora-infra",
    "github_repo": "fmn",
    "page_width": "1040px",
    "show_related": True,
    "sidebar_collapse": True,
}


# -- Extension configuration -------------------------------------------------


source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

myst_enable_extensions = [
    "colon_fence",
]
myst_heading_anchors = 3


# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "fedora-messaging": ("https://fedora-messaging.readthedocs.io/en/latest/", None),
}

extlinks = {
    "commit": ("https://github.com/fedora-infra/fmn/commit/%s", "%s"),
    "issue": ("https://github.com/fedora-infra/fmn/issues/%s", "#%s"),
    "pr": ("https://github.com/fedora-infra/fmn/pull/%s", "PR#%s"),
}

# -- Misc -----


def run_apidoc(_):
    from sphinx.ext import apidoc

    apidoc.main(
        [
            "-f",
            "-o",
            os.path.join(topdir, "docs", "_source"),
            "-T",
            "-e",
            "-M",
            os.path.join(topdir, "fmn"),
            # exclude patterns:
            os.path.join(topdir, "fmn", "database", "migrations"),
            os.path.join(topdir, "fmn", "core", "collectd.py"),
        ]
    )


def setup(app):
    app.connect("builder-inited", run_apidoc)
