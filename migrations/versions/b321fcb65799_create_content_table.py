"""create content table

Revision ID: b321fcb65799
Revises: f03a50c03811
Create Date: 2024-07-20 19:34:50.254398

"""
from typing import Sequence, Union
#from models.tags import DeclarativeBase

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b321fcb65799'
down_revision: Union[str, None] = 'f03a50c03811'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "content",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String),
        sa.Column("content", sa.String),
    )


def downgrade() -> None:
    op.drop_table("content")
