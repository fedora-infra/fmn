"""Get CI error messages

Revision ID: 9987c7c958c7
Revises: 226fd58fe7e5
Create Date: 2017-08-17 12:03:19.100006

"""

# revision identifiers, used by Alembic.
revision = '9987c7c958c7'
down_revision = '226fd58fe7e5'

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

path = 'fmn.rules:ci_step_complete'
target = "Events on packages that I own"


def upgrade():
    """ Update all the filters in the database named after `target` (defined
    above), which happens to be the name of the default config set for all
    packagers, to add a notification to ignore notifications from the CI
    pipeline about steps that completed successfully.
    IE: this migration adds to the default notifications for packager,
    notifications about failed/aborted steps of the CI pipeline.
    """
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
    """ From the default set of notifications for packager, this method removes
    the rule to ignore successfull steps of the CI pipeline.
    """
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
