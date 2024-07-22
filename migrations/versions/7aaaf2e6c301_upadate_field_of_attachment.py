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
    pass


def downgrade() -> None:
    pass
