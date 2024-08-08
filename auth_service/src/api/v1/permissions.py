from fastapi import APIRouter, Depends

from src.schemas.permission import PermissionInDB, PermissionCreate
from src.services.user import get_user_service

router = APIRouter()


@router.post("/", response_model=PermissionInDB)
async def create_permission(
        permission_create: PermissionCreate,
        # credentials: JwtAuthorizationCredentials = Security(access_security),
        user_service=Depends(get_user_service),
):
    return await user_service.create_permission(permission_create)
