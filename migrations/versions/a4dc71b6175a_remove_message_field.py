"""remove message field

Revision ID: a4dc71b6175a
Revises: 5f6dfbdfc79b
Create Date: 2024-07-22 18:55:08.475827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4dc71b6175a'
down_revision: Union[str, None] = '5f6dfbdfc79b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
