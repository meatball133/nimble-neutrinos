"""update tags-message table

Revision ID: 2fb210e79277
Revises: 11c37fa6013f
Create Date: 2024-07-22 12:09:43.141008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2fb210e79277'
down_revision: Union[str, None] = '11c37fa6013f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
