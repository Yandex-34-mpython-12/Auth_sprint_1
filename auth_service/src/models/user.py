import uuid
from datetime import datetime
from typing import List

from sqlalchemy import DateTime, String, func, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.postgres import Base
from src.models.mixins import UserSchemaMixin
from src.utils.hash import verify_password, hash_password


user_permissions_table = Table(
    "user_permissions",
    Base.metadata,
    Column("user_id", ForeignKey("users.users.id"), primary_key=True),
    Column("permission_id", ForeignKey("users.permissions.id"), primary_key=True),
    schema='users',
)


class User(UserSchemaMixin, Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    token: Mapped["Token"] = relationship(back_populates="user")
    permissions: Mapped[List["Permission"]] = relationship(
        secondary=user_permissions_table, back_populates="users"
    )

    def __init__(self, **kwargs) -> None:
        password = kwargs.pop('password')
        kwargs['password'] = hash_password(password)
        super().__init__(**kwargs)

    def check_password(self, password: str) -> bool:
        return verify_password(password, self.password)

    def __repr__(self) -> str:
        return f'<User {self.login}>'


class Permission(UserSchemaMixin, Base):
    __tablename__ = 'permissions'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    codename: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    users: Mapped[List["User"]] = relationship(
        secondary=user_permissions_table, back_populates="permissions"
    )

    def __repr__(self) -> str:
        return f'<Permission {self.name}>'
