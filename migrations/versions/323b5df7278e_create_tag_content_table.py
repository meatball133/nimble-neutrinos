"""create tag-content table

Revision ID: 323b5df7278e
Revises: b321fcb65799
Create Date: 2024-07-20 19:44:40.880183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '323b5df7278e'
down_revision: Union[str, None] = 'b321fcb65799'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tags_messages"
    )


def downgrade() -> None:
    op.drop_table("tags_message")
