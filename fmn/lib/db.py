# -*- coding: utf-8 -*-
# FMN
# Copyright (C) 2017 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""
This module provides a command to configure a database for FMN.
"""
from __future__ import print_function, unicode_literals

import argparse

from fmn.lib import models


def main():
    """
    The entry point for the database commands.
    """
    parser = argparse.ArgumentParser(description='FMN database manager')
    parser.add_argument(
        '--create',
        '-c',
        dest='create',
        action='store_true',
        help='Create the database tables'
    )
    parser.add_argument(
        '--with-dev-data',
        '-d',
        dest='dev',
        action='store_true',
        help='Add some development sample data'
    )
    args = parser.parse_args()

    if args.create:
        models.BASE.metadata.create_all(models.engine)

    if args.dev:
        dev_data()


def dev_data():
    """
    Populate the database with some development data
    """
    session = models.Session()
    models.Context.create(
        session, name="irc", description="Internet Relay Chat",
        detail_name="irc nick", icon="user",
        placeholder="z3r0_c00l",
    )
    models.Context.create(
        session, name="email", description="Electronic Mail",
        detail_name="email address", icon="envelope",
        placeholder="jane@fedoraproject.org",
    )
    models.Context.create(
        session, name="android", description="Google Cloud Messaging",
        detail_name="registration id", icon="phone",
        placeholder="laksdjfasdlfkj183097falkfj109f"
    )
    models.Context.create(
        session, name="desktop", description="fedmsg-notify",
        detail_name="None", icon="console",
        placeholder="There's no need to put a value here"
    )
    models.Context.create(
        session, name="sse", description="server sent events",
        detail_name="None", icon="console",
        placeholder="There's no need to put a value here"
    )
    session.commit()
    models.Session.remove()
