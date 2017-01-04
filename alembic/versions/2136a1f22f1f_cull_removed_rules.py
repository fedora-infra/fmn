"""Cull removed rules

Revision ID: 2136a1f22f1f
Revises: 2ea9623b21fa
Create Date: 2015-01-08 12:23:51.829172

"""
from __future__ import print_function

# revision identifiers, used by Alembic.
revision = '2136a1f22f1f'
down_revision = '2ea9623b21fa'

from alembic import op
import sqlalchemy as sa

import fmn.lib.models


def upgrade():
    engine = op.get_bind().engine
    session = sa.orm.scoped_session(sa.orm.sessionmaker(bind=engine))

    # Find all rules that got removed in this PR and nuke them
    # https://github.com/fedora-infra/fmn.rules/pull/21
    goners = [
        'fmn.rules:pkgdb_acl_user_remove',
        'fmn.rules:pkgdb_branch_clone',
        'fmn.rules:pkgdb_package_retire',
    ]

    for path in goners:
        rules = session.query(fmn.lib.models.Rule)\
            .filter_by(code_path=path).all()
        for rule in rules:
            print("Deleting %r." % rule)
            session.delete(rule)

    # And one of them wasn't actually removed, it was just renamed.
    moves = [
        ('fmn.rules:pkgdb_critpath_update',
         'fmn.rules:pkgdb_package_critpath_update'),
    ]
    for src, dest in moves:
        rules = session.query(fmn.lib.models.Rule)\
            .filter_by(code_path=src).all()
        for rule in rules:
            rule.code_path = dest

    session.commit()


def downgrade():
    pass
