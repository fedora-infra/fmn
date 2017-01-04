"""Add new mdapi rule.

Revision ID: 38c9c18d342e
Revises: 362efe8fd524
Create Date: 2015-11-13 13:49:25.020563

"""
from __future__ import print_function

# revision identifiers, used by Alembic.
revision = '38c9c18d342e'
down_revision = '362efe8fd524'

from alembic import op
import sqlalchemy as sa

path = 'fmn.rules:mdapi_repo_update'
target = "Events on packages that I own"

import fmn.lib
import fmn.lib.models

import fedmsg

# Running this script actually produces fedmsg messages (since the db changes.)
# Start fedmsg in active mode so that it talks to a fedmsg-relay
try:
    fedmsg.init(active=True)
except ValueError:
    pass


def upgrade():
    engine = op.get_bind().engine
    session = sa.orm.scoped_session(sa.orm.sessionmaker(bind=engine))

    valid_paths = fmn.lib.load_rules(root='fmn.rules')

    filters = session.query(fmn.lib.models.Filter).filter_by(name=target).all()
    print("Found %i filters" % len(filters))

    modified = 0
    for filt in filters:
        if len(filt.rules) < 15:
            # Someone has changed this filter dramatically, so let's not mess
            # with it.
            print("Avoiding %r on %r.  Only %i rules present." % (
                filt, filt.preference, len(filt.rules)))
            continue

        modified += 1
        filt.add_rule(session, valid_paths, path, negated=True)

    print("Modified %i filters, total" % modified)
    session.commit()


def downgrade():
    engine = op.get_bind().engine
    session = sa.orm.scoped_session(sa.orm.sessionmaker(bind=engine))

    valid_paths = fmn.lib.load_rules(root='fmn.rules')

    rules = session.query(fmn.lib.models.Rule).filter_by(code_path=path).all()
    print("Found %i rules" % len(rules))

    for rule in rules:
        rule.filter.remove_rule(session, path, rule.id)

    session.commit()
