from datetime import datetime

from fastapi_users_db_sqlalchemy import UUID_ID
from sqlalchemy import func, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .mixins import UserSchemaMixin
from .base import Base


class UserSignIn(UserSchemaMixin, Base):
    __tablename__ = 'user_sign_in'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[UUID_ID] = mapped_column(ForeignKey("users.user.id"))
    logged_in_at: Mapped[datetime] = mapped_column(server_default=func.now())
    user_agent: Mapped[str] = mapped_column()

    def __repr__(self):
        return f'<UserSignIn {self.user_id}:{self.logged_in_at}>'
