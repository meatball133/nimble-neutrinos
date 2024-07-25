"""change from integer to bigint

Revision ID: 548ee8f87feb
Revises: e4e5b6bfab03
Create Date: 2024-07-25 22:54:20.458642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '548ee8f87feb'
down_revision: Union[str, None] = 'e4e5b6bfab03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
