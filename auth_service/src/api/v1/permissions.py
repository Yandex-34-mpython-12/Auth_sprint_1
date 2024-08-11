from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.v1.fastapi_users import current_active_superuser
from src.core.config import settings
from src.models import User
from src.schemas.permission import PermissionInDB, PermissionCreate

router = APIRouter(
    prefix=settings.api.v1.permissions,
    tags=["Permissions"],
)


@router.post("/", response_model=PermissionInDB)
async def create_permission(
        permission_create: PermissionCreate,
        # credentials: JwtAuthorizationCredentials = Security(access_security),
        user_service=Depends(get_user_service),
):
    return await user_service.create_permission(permission_create)


@router.post("")
def create_permission(
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    permission_create: PermissionCreate,
):
    return {
        "messages": ["secret-m1", "secret-m2", "secret-m3"],
        "user": UserRead.model_validate(user),
    }