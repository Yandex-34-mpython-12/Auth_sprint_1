from uuid import UUID

from fastapi import APIRouter, Depends
from src.api.v1.fastapi_users import fastapi_users
from src.core.config import settings
from src.schemas import HistoryRead
from src.schemas.user import UserRead, UserUpdate
from src.services.history import get_history_service, HistoryService

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
)


@router.get('/{id}/login_history', summary='История входа', response_model=list[HistoryRead])
async def user_sign_in_list(
    id: UUID,
    history_svc: HistoryService = Depends(get_history_service),
):
    return await history_svc.get_user_history(id)

# /me
# /{id}
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)
