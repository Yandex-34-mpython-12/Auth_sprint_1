import logging
import uuid
from typing import Optional, TYPE_CHECKING

from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import (
    BaseUserManager,
    UUIDIDMixin, models, exceptions,
)

from src.core.config import settings
from src.models.user import User

if TYPE_CHECKING:
    from fastapi import Request, Response

log = logging.getLogger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_login(
            self,
            user: User,
            request: Optional["Request"] = None,
            response: Optional["Response"] = None,
    ):
        log.warning(
            "User %r logged in.",
            user.id,
        )

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has registered.",
            user.id,
        )

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        # TODO: токен, который можно использовать для верификации, например отправить на email.
        log.warning(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has forgot their password. Reset token: %r",
            user.id,
            token,
        )
