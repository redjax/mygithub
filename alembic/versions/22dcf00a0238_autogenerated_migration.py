"""autogenerated migration

Revision ID: 22dcf00a0238
Revises: 88a1cade3799
Create Date: 2025-02-08 16:38:57.368621

"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '22dcf00a0238'
down_revision: Union[str, None] = '88a1cade3799'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("gh_starred_repo") as batch_op:
        batch_op.alter_column('language',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("gh_starred_repo") as batch_op:
        batch_op.alter_column('language',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###
