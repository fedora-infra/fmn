"""Add a negated column for rules.

Revision ID: 18ebf3181f87
Revises: 4a95022fd7f3
Create Date: 2014-08-22 15:48:08.952913

"""

# revision identifiers, used by Alembic.
revision = '18ebf3181f87'
down_revision = '4a95022fd7f3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('rules', sa.Column('negated', sa.Boolean(), default=False))


def downgrade():
    op.drop_column('rules', 'negated')
