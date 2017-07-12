# -*- coding: utf-8 -*-
#
# This file is part of FMN.
# Copyright (C) 2017 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Suite 500, Boston, MA 02110-1335,  USA
"""Tests for the :mod:`fmn.rules.utils` module."""
from __future__ import unicode_literals

import unittest

from fmn.rules import utils
from fmn.tests import Base


class GetPkgdb2PackagesForTests(Base):
    maxDiff = None

    def setUp(self):
        super(GetPkgdb2PackagesForTests, self).setUp()
        self.config['fmn.rules.utils.use_pagure_for_ownership'] = False
        self.config['fmn.rules.utils.pkgdb_url'] = \
            'https://admin.fedoraproject.org/pkgdb/api'
        self.expected_point_of_contact = {
            'rpms': set([
                'erlang-cache_tab',
                'erlang-p1_sip',
                'erlang-p1_stringprep',
                'erlang-p1_stun',
                'erlang-p1_tls',
                'erlang-p1_xml',
                'erlang-p1_yaml',
                'python-args',
                'python-clint',
                'python-flower',
                'python-fmn',
                'python-fmn-sse',
                'python-invocations',
                'python-matrix-synapse-ldap3',
                'python-pkginfo',
                'python-pymacaroons-pynacl',
                'python-releases',
                'python-sphinxcontrib-fulltoc',
                'python-sqlalchemy_schemadisplay',
                'python-twine',
            ])
        }
        self.expected_comaintained = {
            'rpms': set([
                'bodhi',
                'ejabberd',
                'erlang-esip',
                'erlang-ezlib',
                'erlang-fast_tls',
                'erlang-fast_xml',
                'erlang-fast_yaml',
                'erlang-goldrush',
                'erlang-iconv',
                'erlang-luerl',
                'erlang-oauth2',
                'erlang-p1_iconv',
                'erlang-p1_mysql',
                'erlang-p1_oauth2',
                'erlang-p1_pam',
                'erlang-p1_pgsql',
                'erlang-p1_utils',
                'erlang-p1_xmlrpc',
                'erlang-p1_zlib',
                'erlang-proper',
                'erlang-stringprep',
                'erlang-stun',
                'erlang-xmpp',
                'fegistry',
                'python-crane',
                'python-idna',
                'python-ipdb',
                'python-isodate',
                'python-kaptan',
                'python-pymongo',
                'python-requests',
                'python-rpdb',
                'python-urllib3',
            ])
        }
        self.expected_watch = {'rpms': set(['python-pytoml'])}
        self.expected_all = {
            'rpms': self.expected_watch['rpms'].union(self.expected_comaintained['rpms'].union(
                self.expected_point_of_contact['rpms'])),
        }

    def test_bad_response(self):
        """Assert a bad response results in an empty result."""
        packages = utils._get_pkgdb2_packages_for(self.config, 'thisisnotausername123', [])
        self.assertEqual(dict(), packages)

    def test_watch(self):
        """Assert watch results from pkgdb2 works."""
        packages = utils._get_pkgdb2_packages_for(self.config, 'jcline', ['watch'])
        self.assertEqual(self.expected_watch, packages)

    def test_comaintained(self):
        """Assert co-maintained results from pkgdb2 works."""
        packages = utils._get_pkgdb2_packages_for(self.config, 'jcline', ['co-maintained'])
        self.assertEqual(self.expected_comaintained, packages)

    def test_point_of_contact(self):
        """Assert point of contact results from pkgdb2 works."""
        packages = utils._get_pkgdb2_packages_for(self.config, 'jcline', ['point of contact'])
        self.assertEqual(self.expected_point_of_contact, packages)

    def test_all(self):
        packages = utils._get_pkgdb2_packages_for(
            self.config, 'jcline', ['point of contact', 'watch', 'co-maintained'])
        self.assertEqual(self.expected_all, packages)


class GetPagurePackagesForTests(Base):
    maxDiff = None

    def setUp(self):
        super(GetPagurePackagesForTests, self).setUp()
        self.config['fmn.rules.utils.use_pagure_for_ownership'] = True
        self.config['fmn.rules.utils.pagure_api_url'] = \
            'https://src.stg.fedoraproject.org/pagure/api'
        self.expected_point_of_contact = {
            'rpms': set([
                'erlang-cache_tab',
                'erlang-p1_sip',
                'erlang-p1_stringprep',
                'erlang-p1_stun',
                'erlang-p1_tls',
                'erlang-p1_xml',
                'erlang-p1_yaml',
                'python-args',
                'python-clint',
                'python-flower',
                'python-invocations',
                'python-pkginfo',
                'python-releases',
                'python-sphinxcontrib-fulltoc',
                'python-twine',
            ])
        }
        self.expected_comaintained = {
            'rpms': set([
                'ejabberd',
                'erlang-cache_tab',
                'erlang-esip',
                'erlang-ezlib',
                'erlang-fast_tls',
                'erlang-fast_xml',
                'erlang-fast_yaml',
                'erlang-goldrush',
                'erlang-iconv',
                'erlang-luerl',
                'erlang-oauth2',
                'erlang-p1_iconv',
                'erlang-p1_mysql',
                'erlang-p1_oauth2',
                'erlang-p1_pam',
                'erlang-p1_pgsql',
                'erlang-p1_sip',
                'erlang-p1_stringprep',
                'erlang-p1_stun',
                'erlang-p1_tls',
                'erlang-p1_utils',
                'erlang-p1_xml',
                'erlang-p1_xmlrpc',
                'erlang-p1_yaml',
                'erlang-p1_zlib',
                'erlang-proper',
                'erlang-stringprep',
                'erlang-stun',
                'pulp',
                'pulp-docker',
                'pulp-ostree',
                'pulp-puppet',
                'pulp-python',
                'pulp-rpm',
                'python-args',
                'python-clint',
                'python-crane',
                'python-flower',
                'python-invocations',
                'python-isodate',
                'python-pkginfo',
                'python-pymongo',
                'python-releases',
                'python-rpdb',
                'python-sphinxcontrib-fulltoc',
                'python-twine',
            ])
        }
        self.expected_watch = {}
        self.expected_all = {
            'rpms': self.expected_comaintained['rpms'].union(
                self.expected_point_of_contact['rpms']),
        }

    def test_bad_response(self):
        """Assert a bad response results in an empty result."""
        packages = utils._get_pagure_packages_for(self.config, 'thisisnotausername123', [])
        self.assertEqual(dict(), packages)

    def test_watch(self):
        """Assert watch results from pagure works."""
        packages = utils._get_pagure_packages_for(self.config, 'jcline', ['watch'])
        self.assertEqual(self.expected_watch, packages)

    def test_comaintained(self):
        """Assert co-maintained results from pagure works."""
        packages = utils._get_pagure_packages_for(self.config, 'jcline', ['co-maintained'])
        self.assertEqual(self.expected_comaintained, packages)

    def test_point_of_contact(self):
        """Assert point of contact results from pagure works."""
        packages = utils._get_pagure_packages_for(self.config, 'jcline', ['point of contact'])
        self.assertEqual(self.expected_point_of_contact, packages)

    def test_all(self):
        packages = utils._get_pagure_packages_for(
            self.config, 'jcline', ['point of contact', 'watch', 'co-maintained'])
        self.assertEqual(self.expected_all, packages)


if __name__ == '__main__':
    unittest.main(verbosity=2)
