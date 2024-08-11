# import uuid
# from datetime import datetime
#
# from sqlalchemy import DateTime, func, ForeignKey, BigInteger
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from src.db.postgres import Base
# from .mixins import UserSchemaMixin
#
#
# class Token(UserSchemaMixin, Base):
#     __tablename__ = 'tokens'
#
#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     refresh_token: Mapped[str] = mapped_column(unique=True, nullable=False)
#     user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.users.id'), unique=True)
#     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
#
#     user: Mapped["User"] = relationship(back_populates="token", single_parent=True)
#
#     def __repr__(self) -> str:
#         return f'<Token {self.id}>'
