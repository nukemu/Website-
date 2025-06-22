"""empty message

Revision ID: e9d6feb065fb
Revises: 580a280ffedd
Create Date: 2025-06-19 23:39:41.736522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9d6feb065fb'
down_revision: Union[str, None] = '580a280ffedd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
