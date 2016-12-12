"""Add the verbose column.

Revision ID: 24533471e302
Revises: 59ee93c4bf71
Create Date: 2015-03-20 14:49:57.753166

"""

# revision identifiers, used by Alembic.
revision = '24533471e302'
down_revision = '59ee93c4bf71'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('preferences',
                  sa.Column('verbose', sa.Boolean(), server_default="TRUE"))


def downgrade():
    op.drop_column('preferences', 'verbose')
