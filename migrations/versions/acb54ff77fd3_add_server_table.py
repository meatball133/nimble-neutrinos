"""add server table

Revision ID: acb54ff77fd3
Revises: fc71b2cddb77
Create Date: 2024-07-22 12:15:55.201950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acb54ff77fd3'
down_revision: Union[str, None] = 'fc71b2cddb77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "server",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("discord_id", sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("server")