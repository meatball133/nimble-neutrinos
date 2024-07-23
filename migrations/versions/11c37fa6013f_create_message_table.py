"""create message table

Revision ID: 11c37fa6013f
Revises: 7aaaf2e6c301
Create Date: 2024-07-22 11:58:09.040151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11c37fa6013f'
down_revision: Union[str, None] = '7aaaf2e6c301'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "message",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("author", sa.Integer, nullable=False),
        sa.Column("discord_id", sa.Integer, nullable=False),
        sa.Column("channel_id", sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("message")
