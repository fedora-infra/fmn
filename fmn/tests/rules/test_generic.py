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
"""Tests for the :mod:`fmn.rules.generic` module."""
from __future__ import unicode_literals

import unittest

from fedmsg.meta import make_processors
from fedora.client.fas2 import AccountSystem
import mock

from fmn.rules import generic
from fmn.tests import Base


@mock.patch('fmn.rules.utils._FAS', new=AccountSystem(
    'https://admin.fedoraproject.org/accounts/', username='jcline', password='dummypassword',
    cache_session=False, insecure=False))
class UserPackageFilterTests(Base):

    def setUp(self):
        super(UserPackageFilterTests, self).setUp()
        self.config['fmn.rules.utils.use_pagure_for_ownership'] = False
        self.config['fmn.rules.cache'] = {'backend': 'dogpile.cache.memory'}
        self.config['topic_prefix_re'] = r'org.fedoraproject.prod.*'
        make_processors(**self.config)
        self.rpm_msg = {
            "source_name": "datanommer",
            "i": 1,
            "timestamp": 1490794708.0,
            "msg_id": "2017-9dc3a3f6-4130-401b-865a-5c1240be84cd",
            "topic": "org.fedoraproject.prod.pkgdb.package.branch.new",
            "source_version": "0.6.5",
            "msg": {
                "package_listing": {
                    "status": "Approved",
                    "point_of_contact": "besser82",
                    "package": {
                        "status": "Approved",
                        "upstream_url": "https://github.com/moses-palmer/pystray",
                        "koschei_monitor": True,
                        "monitor": True,
                        "summary": "Provides system tray integration",
                        "namespace": "rpms",
                        "name": "python-pystray",
                        "acls": [],
                        "creation_date": 1490794685.0,
                        "review_url": "https://bugzilla.redhat.com/1436347",
                        "description": "This library allows you to create a system tray icon."
                    },
                    "collection": {
                        "status": "Active",
                        "dist_tag": ".fc25",
                        "koji_name": "f25",
                        "name": "Fedora",
                        "allow_retire": False,
                        "date_updated": "2016-11-22 14:31:43",
                        "version": "25",
                        "date_created": "2016-07-26 13:50:32",
                        "branchname": "f25"
                    },
                    "critpath": False,
                    "status_change": 1490794704.0
                },
                "agent": "limb",
                "package": {
                    "status": "Approved",
                    "upstream_url": "https://github.com/moses-palmer/pystray",
                    "koschei_monitor": True,
                    "monitor": True,
                    "summary": "Provides system tray integration",
                    "namespace": "rpms",
                    "name": "python-pystray",
                    "acls": [],
                    "creation_date": 1490794685.0,
                    "review_url": "https://bugzilla.redhat.com/1436347",
                    "description": "This library allows you to create a system tray icon."
                }
            }
        }

        self.module_msg = {
            "source_name": "datanommer",
            "certificate": "snip",
            "i": 10,
            "timestamp": 1490707946.0,
            "msg_id": "2017-5893b671-d7fd-4334-b600-f5d89e200270",
            "topic": "org.fedoraproject.prod.pkgdb.package.branch.new",
            "source_version": "0.6.5",
            "signature": "snip",
            "msg": {
                "package_listing": {
                    "status": "Approved",
                    "point_of_contact": "ralph",
                    "package": {
                        "status": "Approved",
                        "upstream_url": "",
                        "koschei_monitor": True,
                        "monitor": False,
                        "summary": "PHP scripting language for creating dynamic web sites",
                        "namespace": "modules",
                        "name": "php",
                        "acls": [],
                        "creation_date": 1490707940.0,
                        "review_url": "https://bugzilla.redhat.com/1419506",
                        "description": "snip",
                    },
                    "collection": {
                        "status": "Under Development",
                        "dist_tag": ".fc26",
                        "koji_name": "f26",
                        "name": "Fedora",
                        "allow_retire": True,
                        "date_updated": "2017-02-28 20:24:43",
                        "version": "26",
                        "date_created": "2017-02-28 20:24:57",
                        "branchname": "f26"
                    },
                    "critpath": False,
                    "status_change": 1490707945.0
                },
                "agent": "ralph",
                "package": {
                    "status": "Approved",
                    "upstream_url": "",
                    "koschei_monitor": True,
                    "monitor": False,
                    "summary": "PHP scripting language for creating dynamic web sites",
                    "namespace": "modules",
                    "name": "php",
                    "acls": [],
                    "creation_date": 1490707940.0,
                    "review_url": "https://bugzilla.redhat.com/1419506",
                    "description": "snip",
                }
            }
        }

    def test_no_fasnick(self):
        """Assert if no fasnick is specified, False is returned."""
        self.assertFalse(generic.user_package_filter(self.config, self.rpm_msg))

    def test_empty_message(self):
        """Assert that an empty message results in False."""
        self.assertFalse(generic.user_package_filter(self.config, {}))

    def test_no_matching_packages(self):
        """Assert that a message with no matching packages results in False."""
        self.assertFalse(generic.user_package_filter(self.config, self.rpm_msg, fasnick='jcline'))

    def test_matching_packages(self):
        """Assert that a message with matching packages results in True."""
        self.assertTrue(generic.user_package_filter(self.config, self.rpm_msg, fasnick='besser82'))

    def test_different_namespaces(self):
        """Assert packages with the same name in a different namespace results in False."""
        # remi owns the php RPM, but not the module.
        self.assertFalse(generic.user_package_filter(self.config, self.module_msg, fasnick='remi'))

    def test_namespaces(self):
        """Assert that a message with a namespaced package works correctly."""
        # ralph owns the php module
        self.assertTrue(generic.user_package_filter(self.config, self.module_msg, fasnick='ralph'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
