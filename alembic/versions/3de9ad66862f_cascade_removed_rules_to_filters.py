"""Cascade removed rules to filters

Revision ID: 3de9ad66862f
Revises: 2136a1f22f1f
Create Date: 2015-01-12 15:47:02.778152

"""
from __future__ import print_function

# revision identifiers, used by Alembic.
revision = '3de9ad66862f'
down_revision = '2136a1f22f1f'

from alembic import op
import sqlalchemy as sa

import fmn.lib


def upgrade():
    engine = op.get_bind().engine
    session = sa.orm.scoped_session(sa.orm.sessionmaker(bind=engine))

    # In alembic revision '2136a1f22f1f' these filters has the rules attached
    # that were removed.  The filters need to be removed too.
    goners = [
        'Users removed from packages I own',
        'New branches for packages I own',
        'Retirement of packages I own',
    ]

    for name in goners:
        filters = session.query(fmn.lib.models.Filter)\
            .filter_by(name=name).all()
        for fltr in filters:
            while fltr.rules:
                rule = fltr.rules.pop()
                print("* Deleting rule %r." % rule)
                session.delete(rule)
            print("Deleting filter %r." % fltr)
            session.delete(fltr)
    session.commit()

def downgrade():
    pass
