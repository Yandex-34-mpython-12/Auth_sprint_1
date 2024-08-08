from pydantic import BaseModel


class PermissionCreate(BaseModel):
    name: str
    codename: str


class PermissionInDB(PermissionCreate):
    id: int

    class Config:
        from_attributes = True
