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
"""Tests for :mod:`fmn.celery`."""

import unittest

import mock

from fmn import config, celery as fmn_celery


class ConfigureLoggingTests(unittest.TestCase):

    @mock.patch('fmn.celery.logging.config.dictConfig')
    def test_config_logging(self, mock_dict_config):
        """Assert logging is configured using the app's config."""
        fmn_celery.configure_logging()
        mock_dict_config.assert_called_once_with(config.app_conf['logging'])
