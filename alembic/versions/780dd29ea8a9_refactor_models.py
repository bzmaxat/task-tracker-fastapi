"""refactor models

Revision ID: 780dd29ea8a9
Revises: 18daa7f7a6d0
Create Date: 2025-02-21 16:48:38.202202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '780dd29ea8a9'
down_revision: Union[str, None] = '18daa7f7a6d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
