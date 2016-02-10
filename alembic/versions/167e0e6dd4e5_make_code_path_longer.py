""" Make the code_path column longer.

Revision ID: 167e0e6dd4e5
Revises: 38c9c18d342e
Create Date: 2016-02-08 09:49:53.275987

"""

# revision identifiers, used by Alembic.
revision = '167e0e6dd4e5'
down_revision = '38c9c18d342e'

from alembic import op
import sqlalchemy as sa

def upgrade():
    # First, make this column bigger.
    op.alter_column('rules', 'code_path', type_=sa.String(100))


def downgrade():
    pass
