"""Drop the @mention rule from the defaults.

Revision ID: 1be98d56336
Revises: 1b6e419ea1a6
Create Date: 2015-05-08 16:14:59.310648

"""
from __future__ import print_function

# revision identifiers, used by Alembic.
revision = '1be98d56336'
down_revision = '1b6e419ea1a6'

from alembic import op
import sqlalchemy as sa

import fmn.lib


target = "Mentions of my @username"
pattern_template = "[!-~ ]*[^\w@]@%s[^\w@][!-~ ]*"


def upgrade():
    engine = op.get_bind().engine
    session = sa.orm.scoped_session(sa.orm.sessionmaker(bind=engine))

    filters = session.query(fmn.lib.models.Filter).filter_by(name=target).all()
    print("Found %i filters" % len(filters))

    for filt in filters:
        if not len(filt.rules) == 1:
            # Something is off.  avoid this one.
            print("Avoiding %r on %r" % (filt, filt.preference))
            continue

        for rule in list(filt.rules):
            filt.remove_rule(session, rule.code_path)

        if filt.preference:
            print("Removing %r from %r" % (target, filt.preference))
            filt.preference.filters.remove(filt)

        session.delete(filt)

    session.commit()


def downgrade():
    engine = op.get_bind().engine
    session = sa.orm.scoped_session(sa.orm.sessionmaker(bind=engine))

    valid_paths = fmn.lib.load_rules(root='fmn.rules')

    prefs = session.query(fmn.lib.models.Preference).all()
    print("Found %i prefs" % len(prefs))

    for pref in prefs:
        # Add a special filter that looks for mentions like @ralph
        nick = pref.openid.split('.')[0]
        filt = fmn.lib.models.Filter.create(
            session, "Mentions of my @username")
        pattern = '[!-~ ]*[^\w@]@%s[^\w@][!-~ ]*' % nick
        filt.add_rule(session, valid_paths,
                    "fmn.rules:regex_filter", pattern=pattern)
        pref.add_filter(session, filt, notify=True)
        # END @username filter

    session.commit()
