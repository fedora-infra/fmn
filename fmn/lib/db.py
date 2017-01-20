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

import sys

import fedmsg.config
import fmn.lib.models

def main():
    """
    The entry point for the database commands.
    """
    config = fedmsg.config.load_config()
    uri = config.get('fmn.sqlalchemy.uri')
    if not uri:
        raise ValueError("fmn.sqlalchemy.uri must be present")

    if '-h' in sys.argv or '--help'in sys.argv:
        print(sys.argv[0] + " [--with-dev-data]")
        sys.exit(0)

    session = fmn.lib.models.init(uri, debug=True, create=True)

    if '--with-dev-data' in sys.argv:
        context1 = fmn.lib.models.Context.create(
            session, name="irc", description="Internet Relay Chat",
            detail_name="irc nick", icon="user",
            placeholder="z3r0_c00l",
        )
        context2 = fmn.lib.models.Context.create(
            session, name="email", description="Electronic Mail",
            detail_name="email address", icon="envelope",
            placeholder="jane@fedoraproject.org",
        )
        context3 = fmn.lib.models.Context.create(
            session, name="android", description="Google Cloud Messaging",
            detail_name="registration id", icon="phone",
            placeholder="laksdjfasdlfkj183097falkfj109f"
        )
        context4 = fmn.lib.models.Context.create(
            session, name="desktop", description="fedmsg-notify",
            detail_name="None", icon="console",
            placeholder="There's no need to put a value here"
        )
        context5 = fmn.lib.models.Context.create(
            session, name="sse", description="server sent events",
            detail_name="None", icon="console",
            placeholder="There's no need to put a value here"
        )
        session.commit()
