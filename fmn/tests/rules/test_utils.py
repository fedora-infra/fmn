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

from fedora.client.fas2 import AccountSystem
from requests.exceptions import ConnectTimeout, ReadTimeout
from dogpile import cache
import mock

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

    @mock.patch('fmn.rules.utils._get_pkgdb2_packages_for')
    def test_using_pkgdb(self, mock_get_pkgs):
        utils._get_packages_for(self.config, 'jcline', [])
        mock_get_pkgs.assert_called_once_with(self.config, 'jcline', [])

    def test_bad_response(self):
        """Assert a bad response results in an empty result."""
        packages = utils._get_packages_for(self.config, 'thisisnotausername123', [])
        self.assertEqual(dict(), packages)

    def test_watch(self):
        """Assert watch results from pkgdb2 works."""
        packages = utils._get_packages_for(self.config, 'jcline', ['watch'])
        self.assertEqual(self.expected_watch, packages)

    def test_comaintained(self):
        """Assert co-maintained results from pkgdb2 works."""
        packages = utils._get_packages_for(self.config, 'jcline', ['co-maintained'])
        self.assertEqual(self.expected_comaintained, packages)

    def test_point_of_contact(self):
        """Assert point of contact results from pkgdb2 works."""
        packages = utils._get_packages_for(self.config, 'jcline', ['point of contact'])
        self.assertEqual(self.expected_point_of_contact, packages)

    def test_all(self):
        packages = utils._get_packages_for(
            self.config, 'jcline', ['point of contact', 'watch', 'co-maintained'])
        self.assertEqual(self.expected_all, packages)

    @mock.patch('fmn.rules.utils.requests_session')
    def test_connect_failure(self, mock_session):
        mock_session.get.side_effect = ConnectTimeout
        """Assert a bad response results in an empty result."""
        packages = utils._get_packages_for(self.config, 'jcline', ['co-maintained'])
        self.assertEqual(set(), packages)

    @mock.patch('fmn.rules.utils.requests_session')
    def test_read_failure(self, mock_session):
        """Assert a bad response results in an empty result."""
        mock_session.get.side_effect = ReadTimeout
        packages = utils._get_packages_for(self.config, 'jcline', ['co-maintained'])
        self.assertEqual(set(), packages)


@mock.patch('fmn.rules.utils._FAS', new=AccountSystem(
    'https://admin.fedoraproject.org/accounts/', username='jcline', password='dummypassword',
    cache_session=False, insecure=False))
class GetPkgdb2PackagersForTests(Base):

    def setUp(self):
        super(GetPkgdb2PackagersForTests, self).setUp()

        self.config = {
            'fmn.rules.utils.use_pagure_for_ownership': False,
            'fmn.rules.cache': {'backend': 'dogpile.cache.memory'},
            'fas_credentials': {'username': 'jcline', 'password': 'supersecret'}
        }

    @mock.patch('fmn.rules.utils._get_pkgdb2_packagers_for')
    def test_using_pkgdb(self, mock_get_packagers):
        utils._get_packagers_for(self.config, 'rpms/urllib3')
        mock_get_packagers.assert_called_once_with(self.config, 'rpms/urllib3')

    def test_no_groups(self):
        """Assert packages without groups return the expected set of packagers."""
        expected_packagers = set(['bowlofeggs', 'jcline', 'martinlanghoff', 'peter'])
        packagers = utils._get_packagers_for(self.config, 'rpms/ejabberd')

        self.assertTrue(expected_packagers.issubset(packagers))

    def test_groups(self):
        infra_group = set([
            'abompard',
            'bochecha',
            'bowlofeggs',
            'codeblock',
            'jcline',
            'kevin',
            'lmacken',
            'pingou',
            'puiterwijk',
            'sayanchowdhury',
            'toshio',
        ])
        committers = set([
            'abompard',
            'jcline',
            'ralph',
            'sagarun',
        ])
        expected_packagers = infra_group.union(committers)

        packagers = utils._get_packagers_for(self.config, 'rpms/python-urllib3')

        self.assertTrue(expected_packagers.issubset(packagers))

    def test_no_namespace(self):
        """Assert packages without a namespace default to RPM."""
        expected_packagers = set(['bowlofeggs', 'jcline', 'martinlanghoff', 'peter'])
        packagers = utils._get_packagers_for(self.config, 'ejabberd')
        self.assertTrue(expected_packagers.issubset(packagers))

    @mock.patch('fmn.rules.utils.requests_session')
    def test_read_timeout(self, mock_session):
        mock_session.get.side_effect = ReadTimeout
        packagers = utils._get_packagers_for(self.config, 'rpms/ejabberd')

        self.assertEqual(set(), packagers)

    @mock.patch('fmn.rules.utils.requests_session')
    def test_connect_timeout(self, mock_session):
        mock_session.get.side_effect = ConnectTimeout
        packagers = utils._get_packagers_for(self.config, 'rpms/ejabberd')

        self.assertEqual(set(), packagers)

    def test_error_response(self):
        packagers = utils._get_packagers_for(self.config, 'notanamespace/orapackage')

        self.assertEqual(set(), packagers)


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
                'python-cryptography',
                'python-cryptography-vectors',
                'python-flower',
                'python-invocations',
                'python-pkginfo',
                'python-releases',
                'python-sphinxcontrib-fulltoc',
                'python-twine'
            ])
        }
        self.expected_comaintained = {
            'rpms': set([
                'bodhi',
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
                'python-args',
                'python-chardet',
                'python-clint',
                'python-crane',
                'python-cryptography',
                'python-cryptography-vectors',
                'python-flower',
                'python-idna',
                'python-invocations',
                'python-ipdb',
                'python-isodate',
                'python-pkginfo',
                'python-pymongo',
                'python-pytoml',
                'python-releases',
                'python-requests',
                'python-rpdb',
                'python-sphinxcontrib-fulltoc',
                'python-twine',
                'python-urllib3',
            ])
        }
        self.expected_all = {
            'rpms': self.expected_comaintained['rpms'].union(
                self.expected_point_of_contact['rpms']),
        }

    @mock.patch('fmn.rules.utils._get_pagure_packages_for')
    def test_using_pagure(self, mock_get_packages):
        utils._get_packages_for(self.config, 'jcline', [])
        mock_get_packages.assert_called_once_with(self.config, 'jcline', [])

    def test_bad_response(self):
        """Assert a bad response results in an empty result."""
        packages = utils._get_packages_for(
            self.config, 'thisisnotausername123', ['co-maintained'])
        self.assertEqual(dict(), packages)

    @mock.patch('fmn.rules.utils.requests_session')
    def test_connect_failure(self, mock_session):
        """Assert a bad response results in an empty result."""
        mock_session.get.side_effect = ConnectTimeout
        packages = utils._get_packages_for(self.config, 'jcline', ['co-maintained'])
        self.assertEqual(dict(), packages)

    @mock.patch('fmn.rules.utils.requests_session')
    def test_read_failure(self, mock_session):
        """Assert a bad response results in an empty result."""
        mock_session.get.side_effect = ReadTimeout
        packages = utils._get_packages_for(self.config, 'jcline', ['co-maintained'])
        self.assertEqual(dict(), packages)

    def test_no_flags(self):
        """Assert passing no flags earns the caller a ValueError."""
        self.assertRaises(ValueError, utils._get_packages_for, self.config, 'jcline', [])

    def test_invalid_flags(self):
        """Assert passing an invalid flags earns the caller a ValueError."""
        self.assertRaises(
            ValueError, utils._get_packages_for, self.config, 'jcline', ['flag'])

    def test_comaintained(self):
        """Assert co-maintained results from pagure works."""
        packages = utils._get_packages_for(self.config, 'jcline', ['co-maintained'])
        self.assertEqual(self.expected_comaintained, packages)

    def test_point_of_contact(self):
        """Assert point of contact results from pagure works."""
        packages = utils._get_packages_for(self.config, 'jcline', ['point of contact'])
        self.assertEqual(self.expected_point_of_contact, packages)

    def test_watch(self):
        """Assert "watch" returns an empty set until it's implemented."""
        self.assertEqual({}, utils._get_packages_for(self.config, 'jcline', ['watch']))

    def test_all(self):
        packages = utils._get_packages_for(
            self.config, 'jcline', ['point of contact', 'co-maintained', 'watch'])
        self.assertEqual(self.expected_all, packages)


class GetPagurePackagersForTests(Base):

    def setUp(self):
        super(GetPagurePackagersForTests, self).setUp()

        self.config = {
            'fmn.rules.utils.use_pagure_for_ownership': True,
            'fmn.rules.utils.pagure_api_url': 'https://src.stg.fedoraproject.org/pagure/api',
            'fmn.rules.cache': {'backend': 'dogpile.cache.memory'},
            'fas_credentials': {'username': 'jcline', 'password': 'supersecret'}
        }

    def test_no_groups(self):
        """Assert packages without groups return the expected set of packagers."""
        expected_packagers = set(['bowlofeggs', 'jcline', 'xavierb', 'martinlanghoff', 'peter'])
        packagers = utils._get_packagers_for(self.config, 'rpms/ejabberd')

        self.assertEqual(expected_packagers, packagers)

    def test_groups(self):
        infra_group = set([
            'abompard',
            'bochecha',
            'bowlofeggs',
            'codeblock',
            'jcline',
            'kevin',
            'lmacken',
            'pingou',
            'puiterwijk',
            'sayanchowdhury',
            'toshio',
        ])
        committers = set([
            'abompard',
            'jcline',
            'ralph',
            'sagarun',
        ])

        packagers = utils._get_packagers_for(self.config, 'rpms/python-urllib3')

        self.assertEqual(infra_group.union(committers), packagers)

    def test_no_namespace(self):
        """Assert packages without a namespace default to RPM."""
        expected_packagers = set(['bowlofeggs', 'jcline', 'xavierb', 'martinlanghoff', 'peter'])
        packagers = utils._get_packagers_for(self.config, 'ejabberd')

        self.assertEqual(expected_packagers, packagers)

    @mock.patch('fmn.rules.utils.requests_session')
    def test_read_timeout(self, mock_session):
        mock_session.get.side_effect = ReadTimeout
        packagers = utils._get_packagers_for(self.config, 'rpms/ejabberd')

        self.assertEqual(set(), packagers)

    @mock.patch('fmn.rules.utils.requests_session')
    def test_connect_timeout(self, mock_session):
        mock_session.get.side_effect = ConnectTimeout
        packagers = utils._get_packagers_for(self.config, 'rpms/ejabberd')

        self.assertEqual(set(), packagers)

    def test_error_response(self):
        packagers = utils._get_packagers_for(self.config, 'notanamespace/orapackage')

        self.assertEqual(set(), packagers)


class GetPackagersOfPackageTests(unittest.TestCase):
    """Tests for the :func:`get_packagers_of_package` function."""

    @mock.patch('fmn.rules.utils._get_packagers_for')
    def test_cache_miss(self, mock_get_packagers_for):
        """Assert cache misses result in the value being created."""
        cache_dict = {}
        config = {
            'fmn.rules.cache': {
                'backend': 'dogpile.cache.memory', 'arguments': {'cache_dict': cache_dict}
            }
        }

        with mock.patch('fmn.rules.utils._cache', cache.make_region()):
            packagers = utils.get_packagers_of_package(config, 'some-package')

        mock_get_packagers_for.assert_called_once_with(config, 'some-package')
        self.assertTrue(packagers is mock_get_packagers_for.return_value)

    @mock.patch('fmn.rules.utils._get_packagers_for')
    def test_cache_hit(self, mock_get_packagers_for):
        """Assert cache hits are used and the value isn't recreated."""
        mock_get_packagers_for.return_value = 'jcline'
        cache_dict = {}
        config = {
            'fmn.rules.cache': {
                'backend': 'dogpile.cache.memory', 'arguments': {'cache_dict': cache_dict}
            }
        }

        # We used to call utils.get_packagers_of_package and check that
        # fmn.rules.utils._get_packagers_for had not been called by manually
        # populating the cache first. However, it looks like dogpile.cache
        # changed between its version 0.9.0 and 1.+ which results in the
        # get_or_create method to call _get_packagers_for in 1.+ while it wasn't
        # called in 0.9.0.
        # So as a way to still test the caching, we'll call the function twice
        # and check that at the end the _get_packagers_for function was only
        # called once.

        self.assertEqual(0, mock_get_packagers_for.call_count)
        with mock.patch('fmn.rules.utils._cache', cache.make_region()):
            packagers = utils.get_packagers_of_package(config, 'some-package')
            packagers = utils.get_packagers_of_package(config, 'some-package')
        self.assertEqual(1, mock_get_packagers_for.call_count)
        self.assertEqual('jcline', packagers)


if __name__ == '__main__':
    unittest.main(verbosity=2)
