from typing import Annotated

from fastapi import APIRouter, Depends
from src.api.v1.fastapi_users import current_active_superuser
from src.core.config import settings
from src.models import User
from src.schemas.permission import PermissionCreate, PermissionRead
from src.services.user import get_user_service

router = APIRouter(
    prefix=settings.api.v1.permissions,
    tags=["Permissions"],
)


@router.post("", response_model=PermissionRead)  # TODO: написать тут
async def create_permission(
        permission_create: PermissionCreate,
        user: Annotated[
            User,
            Depends(current_active_superuser),
        ],
        user_service=Depends(get_user_service),
):
    return await user_service.create_permission(permission_create)
