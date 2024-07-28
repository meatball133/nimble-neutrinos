"""add-favorite-table

Revision ID: b31a0489ef30
Revises: 548ee8f87feb
Create Date: 2024-07-28 12:58:04.888966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b31a0489ef30'
down_revision: Union[str, None] = '548ee8f87feb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
