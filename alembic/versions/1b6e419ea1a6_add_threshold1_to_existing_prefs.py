"""Add threshold1 to existing prefs.

Revision ID: 1b6e419ea1a6
Revises: 24533471e302
Create Date: 2015-05-05 10:11:55.738516

"""
from __future__ import print_function

# revision identifiers, used by Alembic.
revision = '1b6e419ea1a6'
down_revision = '24533471e302'

from alembic import op
import sqlalchemy as sa

import fmn.lib
import fmn.lib.models

import fedmsg

# Running this script actually produces fedmsg messages (since the db changes.)
# Start fedmsg in active mode so that it talks to a fedmsg-relay
try:
    fedmsg.init(active=True)
except ValueError:
    pass

new_rules = [
    'fmn.rules:faf_report_threshold1',
    'fmn.rules:faf_problem_threshold1',
]

target = 'Events on packages that I own'

def upgrade():
    engine = op.get_bind().engine
    session = sa.orm.scoped_session(sa.orm.sessionmaker(bind=engine))

    valid_paths = fmn.lib.load_rules(root='fmn.rules')

    filters = session.query(fmn.lib.models.Filter).filter_by(name=target).all()
    print("Found %i filters" % len(filters))

    for filt in filters:
        print("%r has %r rules" % (filt, len(filt.rules)))
        for path in new_rules:
            filt.add_rule(session, valid_paths, path, negated=True)

    session.commit()


def downgrade():
    engine = op.get_bind().engine
    session = sa.orm.scoped_session(sa.orm.sessionmaker(bind=engine))

    filters = session.query(fmn.lib.models.Filter).filter_by(name=target).all()
    print("Found %i filters" % len(filters))

    for filt in filters:
        for path in new_rules:
            try:
                filt.remove_rule(session, path)
            except ValueError as e:
                print("warning: ", str(e))

    session.commit()
