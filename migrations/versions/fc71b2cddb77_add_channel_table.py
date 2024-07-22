"""add channel table

Revision ID: fc71b2cddb77
Revises: 0072c2e91735
Create Date: 2024-07-22 12:14:31.647125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc71b2cddb77'
down_revision: Union[str, None] = '0072c2e91735'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "channel",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("discord_id", sa.Integer, nullable=False),
        sa.Column("enabled", sa.Boolean, nullable=False),
        sa.Column("server_id", sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("channel")
