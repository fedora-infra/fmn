# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

"""Rule.name is optional

Revision ID: 85ea1d6c9a3f
Revises: 59e22969e199
Create Date: 2023-04-04 12:25:42.770059
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "85ea1d6c9a3f"
down_revision = "59e22969e199"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("rules", "name", existing_type=sa.TEXT(), nullable=True)


def downgrade():
    op.alter_column("rules", "name", existing_type=sa.TEXT(), nullable=False)
