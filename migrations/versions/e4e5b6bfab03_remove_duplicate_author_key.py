"""remove duplicate author key

Revision ID: e4e5b6bfab03
Revises: bd9dde6541b4
Create Date: 2024-07-23 16:56:25.110399

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4e5b6bfab03'
down_revision: Union[str, None] = 'bd9dde6541b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
