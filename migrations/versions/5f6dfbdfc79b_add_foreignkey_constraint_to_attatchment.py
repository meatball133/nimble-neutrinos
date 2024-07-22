"""add foreignkey constraint to attatchment

Revision ID: 5f6dfbdfc79b
Revises: 8b66ab341111
Create Date: 2024-07-22 12:34:35.593561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f6dfbdfc79b'
down_revision: Union[str, None] = '8b66ab341111'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
