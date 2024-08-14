"""Initial migration

Revision ID: 88a9d225f5ca
Revises: 
Create Date: 2024-08-14 14:43:07.251507

"""

from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa


revision: str = "88a9d225f5ca"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("create schema users")
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        schema="users",
    )
    op.create_table(
        "user",
        sa.Column("role_id", sa.Integer(), nullable=True),
        sa.Column(
            "id", fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False
        ),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=1024), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["users.roles.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="users",
    )
    op.create_index(
        op.f("ix_users_user_email"),
        "user",
        ["email"],
        unique=True,
        schema="users",
    )
    op.create_table(
        "user_sign_in",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column(
            "user_id",
            fastapi_users_db_sqlalchemy.generics.GUID(),
            nullable=False,
        ),
        sa.Column(
            "logged_in_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("user_agent", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="users",
    )


def downgrade() -> None:
    op.drop_table("user_sign_in", schema="users")
    op.drop_index(
        op.f("ix_users_user_email"), table_name="user", schema="users"
    )
    op.drop_table("user", schema="users")
    op.drop_table("roles", schema="users")
    op.execute("drop schema users")
