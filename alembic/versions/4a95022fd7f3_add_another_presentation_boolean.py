"""Add another presentation boolean.

Revision ID: 4a95022fd7f3
Revises: 33082c0ecf3f
Create Date: 2014-06-10 11:10:30.437910

"""

# revision identifiers, used by Alembic.
revision = '4a95022fd7f3'
down_revision = '33082c0ecf3f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('preferences', sa.Column('markup_messages', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('preferences', 'markup_messages')
