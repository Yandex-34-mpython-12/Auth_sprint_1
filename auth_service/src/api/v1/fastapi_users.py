import uuid

from fastapi_users import FastAPIUsers

from src.models import User

from src.api.dependencies.authentication import get_user_manager
from src.api.dependencies.authentication import authentication_backend

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [authentication_backend],
)

current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)
