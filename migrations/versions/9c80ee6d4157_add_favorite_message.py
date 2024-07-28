"""add favorite message

Revision ID: 9c80ee6d4157
Revises: 548ee8f87feb
Create Date: 2024-07-28 10:36:28.120050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c80ee6d4157'
down_revision: Union[str, None] = '548ee8f87feb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("message", sa.Column("favorite", sa.Boolean, default=False))


def downgrade() -> None:
    op.drop_column("message", "favorite")
