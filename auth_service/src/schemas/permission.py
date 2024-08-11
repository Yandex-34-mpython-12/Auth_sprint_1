from pydantic import BaseModel


class BasePermission(BaseModel):
    name: str
    codename: str


class PermissionRead(BasePermission):
    id: int


class PermissionCreate(BasePermission):
    pass


class PermissionUpdate(BasePermission):
    pass
