import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.postgres import Base
from utils.hash import verify_password, hash_password


class UserSchemaMixin:
    __table_args__ = {'schema': 'users'}


class User(UserSchemaMixin, Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    token: Mapped["Token"] = relationship(back_populates="user")

    def __init__(self, **kwargs) -> None:
        password = kwargs.pop('password')
        kwargs['password'] = hash_password(password)
        super().__init__(**kwargs)

    def check_password(self, password: str) -> bool:
        return verify_password(password, self.password)

    def __repr__(self) -> str:
        return f'<User {self.login}>'


class Token(UserSchemaMixin, Base):
    __tablename__ = 'tokens'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    refresh_token: Mapped[str] = mapped_column(unique=True, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.users.id'), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="token", single_parent=True)

    def __repr__(self) -> str:
        return f'<Token {self.id}>'
