"""create message table

Revision ID: 11c37fa6013f
Revises: 7aaaf2e6c301
Create Date: 2024-07-22 11:58:09.040151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11c37fa6013f'
down_revision: Union[str, None] = '7aaaf2e6c301'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
