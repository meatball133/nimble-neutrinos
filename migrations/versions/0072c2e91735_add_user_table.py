"""add user table

Revision ID: 0072c2e91735
Revises: 2fb210e79277
Create Date: 2024-07-22 12:12:58.653505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0072c2e91735'
down_revision: Union[str, None] = '2fb210e79277'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("discord_id", sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("user")
