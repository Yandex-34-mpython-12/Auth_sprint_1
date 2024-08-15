"""Add partitions to user_sign_in

Revision ID: 723779cf865a
Revises: 78381f0b11f2
Create Date: 2024-08-15 14:38:20.387963

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "723779cf865a"
down_revision: Union[str, None] = "78381f0b11f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS users.user_sign_in_smart PARTITION OF users.user_sign_in 
        FOR VALUES IN ('smart')
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS users.user_sign_in_mobile PARTITION OF users.user_sign_in 
        FOR VALUES IN ('mobile')
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS users.user_sign_in_web PARTITION OF users.user_sign_in 
        FOR VALUES IN ('web')
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS users.user_sign_in_smart;")
    op.execute("DROP TABLE IF EXISTS users.user_sign_in_mobile;")
    op.execute("DROP TABLE IF EXISTS users.user_sign_in_web;")
