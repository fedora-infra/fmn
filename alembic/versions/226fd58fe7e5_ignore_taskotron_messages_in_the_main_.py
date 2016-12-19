"""Ignore taskotron messages in the main filter.

Revision ID: 226fd58fe7e5
Revises: 5403906cbd9f
Create Date: 2016-02-11 07:54:04.350712

"""
from __future__ import print_function

# revision identifiers, used by Alembic.
revision = '226fd58fe7e5'
down_revision = '5403906cbd9f'

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

target = 'Events on packages that I own'
path = 'fmn.rules:taskotron_result_new'

def upgrade():
    engine = op.get_bind().engine
    session = sa.orm.scoped_session(sa.orm.sessionmaker(bind=engine))

    valid_paths = fmn.lib.load_rules(root='fmn.rules')

    filters = session.query(fmn.lib.models.Filter).filter_by(name=target).all()
    print("Found %i filters" % len(filters))

    for filt in filters:
        print("%r has %r rules" % (filt, len(filt.rules)))
        filt.add_rule(session, valid_paths, path, negated=True)

    session.commit()


def downgrade():
    engine = op.get_bind().engine
    session = sa.orm.scoped_session(sa.orm.sessionmaker(bind=engine))

    filters = session.query(fmn.lib.models.Filter).filter_by(name=target).all()
    print("Found %i filters" % len(filters))

    for filt in filters:
        for rule in filt.rules:
            if rule.code_path == path:
                print("Removing %r from %r" % (path, filt))
                filt.remove_rule(session, path, rule.id)
                break

    session.commit()
