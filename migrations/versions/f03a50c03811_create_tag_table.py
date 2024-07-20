"""create tag table

Revision ID: f03a50c03811
Revises: 
Create Date: 2024-07-20 19:27:57.337240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f03a50c03811'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tag",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String),
        
    )


def downgrade() -> None:
    op.drop_table("tag")
