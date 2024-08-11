from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from auth_service.src.models import Role, User
from src.db.postgres import db_helper



class RoleService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_role_by_name(self, name: str) -> Role:
        result = await self.db.execute(select(Role).where(Role.name == name))
        found = result.scalars().first()

        return found

    async def create_role(self, name: str) -> Optional[Role]:
        if await self.get_role_by_name(name=name):
            return None
        role = Role(name=name)
        self.db.add(role)
        await self.db.commit()
        return role

    async def get_roles(self) -> list[Role]:
        data = await self.db.execute(select(Role))
        return data.scalars().all()

    async def delete_role(self, role_id: int) -> bool:
        result = await self.db.execute(delete(Role).where(Role.id == role_id))
        await self.db.commit()
        return bool(result)

    async def set_user_role(self, user: User, role: Role) -> User:
        ...

    async def delete_user_role(self, user: User, role: Role) -> User:
        ...

    async def get_role_by_id(self, role_id: int) -> Role:
        result = await self.db.execute(select(Role).where(Role.id == role_id))
        role_found = result.scalars().first()
        return role_found if role_found else None


@lru_cache()
def role_services(
    db: AsyncSession = Depends(db_helper.session_getter),
) -> RoleService:
    return RoleService(db=db)