from enum import Enum
from uuid import UUID

from fastapi import Request
from pydantic import Field

from .base import BaseOrjsonModel


class User(BaseOrjsonModel):
    uuid: UUID = Field(..., alias="sub")
    role: "UserRole" = Field(..., alias="role")


class UserRole(Enum):
    anonymous: str = 'anonymous'
    admin: str = 'admin'
    user: str = 'user'
    subscriber: str = 'subscriber'


class AuthRequest(Request):
    custom_user: User
