"""add foreignkey constraint to attachment

Revision ID: f13692d81345
Revises: acb54ff77fd3
Create Date: 2024-07-22 12:17:48.132148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f13692d81345'
down_revision: Union[str, None] = 'acb54ff77fd3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
