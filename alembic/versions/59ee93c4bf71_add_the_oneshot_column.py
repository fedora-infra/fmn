"""Add the oneshot column.

Revision ID: 59ee93c4bf71
Revises: 3de9ad66862f
Create Date: 2015-03-20 13:38:03.081566

"""

# revision identifiers, used by Alembic.
revision = '59ee93c4bf71'
down_revision = '3de9ad66862f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('filters', sa.Column('oneshot', sa.Boolean(), nullable=True, default=False))


def downgrade():
    op.drop_column('filters', 'oneshot')
