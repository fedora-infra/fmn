import sys

import fedmsg.config
import fmn.lib.models

config = fedmsg.config.load_config()
uri = config.get('fmn.sqlalchemy.uri')
if not uri:
    raise ValueError("fmn.sqlalchemy.uri must be present")

session = fmn.lib.models.init(uri, debug=True, create=True)

if '--with-dev-data' in sys.argv:
    user1 = fmn.lib.models.User.get_or_create(session, username="ralph")
    user2 = fmn.lib.models.User.get_or_create(session, username="toshio")
    user3 = fmn.lib.models.User.get_or_create(session, username="toshio")

    context1 = fmn.lib.models.Context.create(
        session, name="irc", description="Internet Relay Chat")
    context2 = fmn.lib.models.Context.create(
        session, name="email", description="Electronic Mail")
    context3 = fmn.lib.models.Context.create(
        session, name="gcm", description="Google Cloud Messaging")

    prefs1 = fmn.lib.models.Preference.create(
        session,
        user=user1,
        context=context1,
        delivery_detail=dict(
            ircnick="threebean",
        )
    )
    prefs2 = fmn.lib.models.Preference.create(
        session,
        user=user1,
        context=context2,
        delivery_detail=dict(
            address="ralph@fedoraproject.org",
        )
    )
    session.commit()
