from typing import Optional

from fastapi_users.models import ID, UP
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from src.models import Role


class AuthUserService(SQLAlchemyUserDatabase):
    async def get(self, id: ID) -> Optional[UP]:
        statement = (
            select(self.user_table)
            .options(
                selectinload(self.user_table.roles).selectinload(Role.permissions)
            )
            .where(self.user_table.id == id)
        )
        user = await self._get_user(statement)
        return user

    async def get_by_email(self, email: str) -> Optional[UP]:
        statement = (
            select(self.user_table)
            .options(
                selectinload(self.user_table.roles).selectinload(Role.permissions)
            )
            .where(func.lower(self.user_table.email) == func.lower(email))
        )
        user = await self._get_user(statement)
        return user
