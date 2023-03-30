# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

"""Add the generated table

Revision ID: 59e22969e199
Revises: a6c12ef04ee5
Create Date: 2023-02-03 14:04:42.631498
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "59e22969e199"
down_revision = "a6c12ef04ee5"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "generated",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("rule_id", sa.Integer(), nullable=False),
        sa.Column("when", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("count", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["rule_id"], ["rules.id"], name=op.f("generated_rule_id_rules_fkey"), ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("generated_pkey")),
    )
    op.create_index(op.f("generated_when_index"), "generated", ["when"], unique=False)


def downgrade():
    op.drop_index(op.f("generated_when_index"), table_name="generated")
    op.drop_table("generated")
