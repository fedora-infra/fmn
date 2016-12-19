"""Add new taskotron filter.

Revision ID: 5403906cbd9f
Revises: 167e0e6dd4e5
Create Date: 2016-02-10 07:55:27.687188

"""
from __future__ import print_function

# revision identifiers, used by Alembic.
revision = '5403906cbd9f'
down_revision = '167e0e6dd4e5'

from alembic import op
import sqlalchemy as sa

import fmn.lib

import fedmsg

# Running this script actually produces fedmsg messages (since the db changes.)
# Start fedmsg in active mode so that it talks to a fedmsg-relay
try:
    fedmsg.init(active=True)
except ValueError:
    pass

filter_name = "Critical taskotron tasks on my packages"

def upgrade():
    engine = op.get_bind().engine
    session = sa.orm.scoped_session(sa.orm.sessionmaker(bind=engine))

    paths = fmn.lib.load_rules(root='fmn.rules')

    # We're going to add a new filter to every user's contexts
    prefs = session.query(fmn.lib.models.Preference).all()

    for pref in prefs:
        fasnick = pref.openid.split('.')[0]
        print("* Handling", fasnick)
        filt = fmn.lib.models.Filter.create(session, filter_name)
        filt.add_rule(session, paths,
                      "fmn.rules:user_package_filter",
                      fasnick=fasnick)
        filt.add_rule(session, paths,
                      "fmn.rules:taskotron_release_critical_task")
        filt.add_rule(session, paths,
                      "fmn.rules:taskotron_task_particular_or_changed_outcome",
                      outcome='FAILED')
        pref.add_filter(session, filt, notify=True)

def downgrade():
    engine = op.get_bind().engine
    session = sa.orm.scoped_session(sa.orm.sessionmaker(bind=engine))

    filters = session.query(fmn.lib.models.Filter)\
        .filter_by(name=filter_name).all()

    for fltr in filters:
        while fltr.rules:
            rule = fltr.rules.pop()
            print("* Deleting rule %r." % rule)
            session.delete(rule)
        print("Deleting filter %r." % fltr)
        session.delete(fltr)

    session.commit()
