"""upadate field of attachment

Revision ID: 7aaaf2e6c301
Revises: 3667668fc3a2
Create Date: 2024-07-22 11:53:20.464960

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7aaaf2e6c301'
down_revision: Union[str, None] = '3667668fc3a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("attachment", "content", new_column_name="message")
    op.drop_column("attachment", "name")
    op.add_column("attachment", sa.Column("discord_id", sa.Integer))
    op.add_column("attachment", sa.Column("message_id", sa.Integer))



def downgrade() -> None:
    op.alter_column("attachment", "message", new_column_name="content")
    op.add_column("attachment", sa.Column("name", sa.String))
    op.drop_column("attachment", "discord_id")
