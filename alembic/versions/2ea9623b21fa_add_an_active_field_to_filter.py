"""Add an active field to Filter

Revision ID: 2ea9623b21fa
Revises: 18ebf3181f87
Create Date: 2014-09-03 09:37:39.653039

"""

# revision identifiers, used by Alembic.
revision = '2ea9623b21fa'
down_revision = '18ebf3181f87'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'filters',
        sa.Column(
            'active',
            sa.Boolean(),
            server_default=sa.sql.expression.true(),
            nullable=False)
    )


def downgrade():
    op.drop_column('filters', 'active')
