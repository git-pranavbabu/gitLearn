"""add user_id column to post table

Revision ID: 47d4b07b6036
Revises: 6573fa7f3985
Create Date: 2025-12-26 19:14:41.524118

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47d4b07b6036'
down_revision: Union[str, Sequence[str], None] = '6573fa7f3985'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key("post_user", "posts", "users", ["user_id"], ["id"], ondelete="CASCADE")



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("post_user", "posts", type_="foreignkey")
    op.drop_column("posts", "user_id")
