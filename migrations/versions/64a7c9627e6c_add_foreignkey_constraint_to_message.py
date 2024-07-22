"""add foreignkey constraint to message

Revision ID: 64a7c9627e6c
Revises: f13692d81345
Create Date: 2024-07-22 12:21:03.130041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64a7c9627e6c'
down_revision: Union[str, None] = 'f13692d81345'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
