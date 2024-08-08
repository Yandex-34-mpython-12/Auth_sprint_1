from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    login: str
    password: str
    first_name: str
    last_name: str


class UserInDB(BaseModel):
    id: UUID
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    login: str
    password: str


class UserPermissionAdd(BaseModel):
    user_id: UUID
    permission_id: int


class UserPermissionInDB(UserPermissionAdd):
    pass
