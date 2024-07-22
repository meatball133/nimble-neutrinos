"""add foreignkey constraint to attachment

Revision ID: f13692d81345
Revises: acb54ff77fd3
Create Date: 2024-07-22 12:17:48.132148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f13692d81345'
down_revision: Union[str, None] = 'acb54ff77fd3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(
        "fk_message_id",
        "attachment",
        "message",
        ["message_id"],
        ["id"],
        onupdate = "CASCADE",
        ondelete = "CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("fk_message_id", "attachment", type_="foreignkey")
