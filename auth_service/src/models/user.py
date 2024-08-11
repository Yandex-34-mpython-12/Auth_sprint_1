from fastapi_users_db_sqlalchemy import UUID_ID, SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import UserSchemaMixin


class User(UserSchemaMixin, SQLAlchemyBaseUserTableUUID, Base):
    roles: Mapped[list["Role"]] = relationship(secondary="users.user_roles", back_populates="users")

    @property
    def roles_as_json(self):
        return {role.name: [perm.codename for perm in role.permissions] for role in self.roles}

    def __repr__(self) -> str:
        return f'<User: {self.email}>'


class Role(UserSchemaMixin, Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    users: Mapped[list["User"]] = relationship(secondary="users.user_roles", back_populates="roles")
    permissions: Mapped[list["Permission"]] = relationship(back_populates="role")


class Permission(UserSchemaMixin, Base):
    __tablename__ = 'permissions'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    codename: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("users.roles.id"), nullable=False)

    role: Mapped["Role"] = relationship(back_populates="permissions")

    def __repr__(self) -> str:
        return f'<Permission: {self.name}>'


class UserRoles(UserSchemaMixin, Base):
    __tablename__ = "user_roles"

    user_id: Mapped[UUID_ID] = mapped_column(ForeignKey("users.user.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("users.roles.id"), primary_key=True)
