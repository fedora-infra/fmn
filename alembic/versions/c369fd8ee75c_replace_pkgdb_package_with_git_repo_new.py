"""
Since pkgdb was retired, the pkgdb.package.new message was replaced with
pagure.project.new. Update the rules accordingly.

Revision ID: c369fd8ee75c
Revises: 9987c7c958c7
Create Date: 2018-03-28 15:08:24.848222
"""
from alembic import op

revision = 'c369fd8ee75c'
down_revision = '9987c7c958c7'

# Key is the old rule, value is the new rule
rule_changes = {
    'fmn.rules:pkgdb_package_new': 'fmn.rules:git_repo_new',
}


def upgrade():
    """Update rule paths that have changed due to pkgdb retirement."""
    for old, new in rule_changes.items():
        sql_statement = """
            UPDATE rules
            SET code_path="{new}"
            WHERE code_path="{old}"
        """.format(old=old, new=new)

        op.execute(sql_statement)


def downgrade():
    """Undo update to rule paths that have changed due to pkgdb retirement."""
    for old, new in rule_changes.items():
        sql_statement = """
            UPDATE rules
            SET code_path="{old}"
            WHERE code_path="{new}"
        """.format(old=old, new=new)

        op.execute(sql_statement)
