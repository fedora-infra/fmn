"""Add new masher rules.

Revision ID: 362efe8fd524
Revises: 1be98d56336
Create Date: 2015-08-26 21:10:25.561878

"""
from __future__ import print_function

# revision identifiers, used by Alembic.
revision = '362efe8fd524'
down_revision = '1be98d56336'

from alembic import op
import sqlalchemy as sa

import fmn.lib


path = 'fmn.rules:bodhi_masher_start'
target = "Events on packages that I own"


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
        rule.filter.remove_rule(session, path)

    session.commit()

