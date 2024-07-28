"""add-favorite-table

Revision ID: b31a0489ef30
Revises: 548ee8f87feb
Create Date: 2024-07-28 12:58:04.888966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b31a0489ef30'
down_revision: Union[str, None] = '548ee8f87feb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "favorite",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("message_id", sa.Integer, sa.ForeignKey("message.id")),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id")),
    )


def downgrade() -> None:
    op.drop_table("favorite")
