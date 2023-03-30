# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

"""Create Rule.disabled

Revision ID: a6c12ef04ee5
Revises: 7b47f8356d9f
Create Date: 2022-12-12 14:21:30.627509
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a6c12ef04ee5"
down_revision = "7b47f8356d9f"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "rules",
        sa.Column("disabled", sa.Boolean(), server_default=sa.text("FALSE"), nullable=False),
    )
    op.create_index(op.f("rules_disabled_index"), "rules", ["disabled"], unique=False)


def downgrade():
    op.drop_index(op.f("rules_disabled_index"), table_name="rules")
    op.drop_column("rules", "disabled")
