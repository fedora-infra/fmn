#!/usr/bin/env python
import sys

import fedmsg.config
import fmn.lib.models

config = fedmsg.config.load_config()
uri = config.get('fmn.sqlalchemy.uri')
if not uri:
    raise ValueError("fmn.sqlalchemy.uri must be present")

if '-h' in sys.argv or '--help'in sys.argv:
    print "createdb.py [--with-dev-data]"
    sys.exit(0)

session = fmn.lib.models.init(uri, debug=True, create=True)

if '--with-dev-data' in sys.argv:
    user1 = fmn.lib.models.User.get_or_create(session, username="ralph")
    user2 = fmn.lib.models.User.get_or_create(session, username="toshio")
    user3 = fmn.lib.models.User.get_or_create(session, username="toshio")

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
        session, name="gcm", description="Google Cloud Messaging",
        detail_name="registration id", icon="phone",
        placeholder="laksdjfasdlfkj183097falkfj109f"
    )

    prefs1 = fmn.lib.models.Preference.create(
        session,
        user=user1,
        context=context1,
        detail_value="threebean",
    )
    prefs2 = fmn.lib.models.Preference.create(
        session,
        user=user1,
        context=context2,
        detail_value="ralph@fedoraproject.org",
    )
    session.commit()
