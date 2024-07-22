"""add foreignkey constraint to channel

Revision ID: 8b66ab341111
Revises: 64a7c9627e6c
Create Date: 2024-07-22 12:28:03.537042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b66ab341111'
down_revision: Union[str, None] = '64a7c9627e6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(
        "fk_server_id",
        "channel",
        "server",
        ["server_id"],
        ["id"],
        onupdate = "CASCADE",
        ondelete = "CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("fk_server_id", "channel", type_="foreignkey")
