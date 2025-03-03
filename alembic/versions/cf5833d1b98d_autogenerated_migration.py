"""autogenerated migration

Revision ID: cf5833d1b98d
Revises: e8167c89b646
Create Date: 2025-02-22 12:08:43.450111

"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "cf5833d1b98d"
down_revision: Union[str, None] = "e8167c89b646"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("gh_repo_owner") as batch_op:
        batch_op.alter_column(
            "user_view_type", existing_type=sa.VARCHAR(), nullable=True
        )
    with op.batch_alter_table("gh_starred_repo") as batch_op:
        batch_op.add_column(sa.Column("has_issues", sa.BOOLEAN(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("gh_starred_repo") as batch_op:
        batch_op.drop_column("has_issues")

    with op.batch_alter_table("gh_repo_owner") as batch_op:
        batch_op.alter_column(
            "user_view_type", existing_type=sa.VARCHAR(), nullable=False
        )
    # ### end Alembic commands ###
