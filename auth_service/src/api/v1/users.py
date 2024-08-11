from fastapi import APIRouter

from src.api.v1.fastapi_users import fastapi_users
from src.core.config import settings
from src.schemas.user import (
    UserRead,
    UserUpdate,
)

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
)

# /me
# /{id}
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)
