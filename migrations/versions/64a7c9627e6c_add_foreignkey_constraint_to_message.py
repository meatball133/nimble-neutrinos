"""add foreignkey constraint to message

Revision ID: 64a7c9627e6c
Revises: f13692d81345
Create Date: 2024-07-22 12:21:03.130041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64a7c9627e6c'
down_revision: Union[str, None] = 'f13692d81345'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("message", sa.Column("user_id", sa.Integer))
    op.create_foreign_key(
        "fk_user_id",
        "message",
        "user",
        ["user_id"],
        ["id"],
        onupdate = "CASCADE",
        ondelete = "CASCADE",
    )

    op.create_foreign_key(
        "fk_channel_id",
        "message",
        "channel",
        ["channel_id"],
        ["id"],
        onupdate = "CASCADE",
        ondelete = "CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("fk_user_id", "message", type_="foreignkey")
    op.drop_column("message", "user_id")
    op.drop_constraint("fk_channel_id", "message", type_="foreignkey")
