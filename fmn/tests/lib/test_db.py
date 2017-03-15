# -*- coding: utf-8 -*-
#
# This file is part of the FMN project.
# Copyright (C) 2017 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""Unit tests for the :mod:`fmn.lib.db` module."""

import unittest

import mock

from fmn.lib import db, models
from fmn.tests import Base as BaseTestCase


class MainTests(BaseTestCase):
    """Tests for the DB CLI entry point"""

    @mock.patch('sys.argv', ['fmn-createdb'])
    @mock.patch('fmn.lib.db.dev_data')
    @mock.patch('fmn.lib.db.models.BASE.metadata.create_all')
    def test_main_no_create_no_dev_data(self, mock_create, mock_dev_data):
        """Assert nothing happens without some arguments"""
        db.main()
        self.assertEqual(0, mock_create.call_count)
        self.assertEqual(0, mock_dev_data.call_count)

    @mock.patch('sys.argv', 'fmn-createdb --with-dev-data'.split())
    @mock.patch('fmn.lib.db.models.BASE.metadata.create_all')
    def test_main_no_create_dev_data(self, mock_create):
        """Assert --with-dev-data adds data"""
        contexts = models.Session.query(models.Context).all()
        self.assertEqual(0, len(contexts))
        db.main()
        self.assertEqual(0, mock_create.call_count)
        contexts = models.Session.query(models.Context).all()
        self.assertEqual(5, len(contexts))

    @mock.patch('sys.argv', 'fmn-createdb --create --with-dev-data'.split())
    @mock.patch('fmn.lib.db.models.BASE.metadata.create_all')
    def test_main_create_dev_data(self, mock_create):
        """Assert -c -d creates a db and adds data"""
        contexts = models.Session.query(models.Context).all()
        self.assertEqual(0, len(contexts))
        db.main()
        mock_create.assert_called_once_with(models.engine)
        contexts = models.Session.query(models.Context).all()
        self.assertEqual(5, len(contexts))


if __name__ == '__main__':
    unittest.main(verbosity=2)
