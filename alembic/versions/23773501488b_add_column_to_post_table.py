"""add column to post table

Revision ID: 23773501488b
Revises: 33a0f02a1e57
Create Date: 2025-12-26 19:05:57.598966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23773501488b'
down_revision: Union[str, Sequence[str], None] = '33a0f02a1e57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("rating", sa.Integer(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "rating")
