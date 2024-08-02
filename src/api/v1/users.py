from datetime import timedelta

from fastapi import APIRouter, status, Depends, HTTPException, Security, Request
from fastapi.responses import JSONResponse
from fastapi_jwt import JwtAccessBearerCookie, JwtRefreshBearer, JwtAuthorizationCredentials

from core.config import settings
from schemas.entity import UserInDB, UserCreate, UserLogin
from schemas.token import Tokens
from services.user import get_user_service

router = APIRouter()


# Read access token from bearer header and cookie (bearer priority)
access_security = JwtAccessBearerCookie(
    secret_key=settings.token_secret_key,
    auto_error=False,
    access_expires_delta=timedelta(hours=1)  # change access token validation timedelta
)
# Read refresh token from bearer header only
refresh_security = JwtRefreshBearer(
    secret_key=settings.token_secret_key,
    auto_error=True  # automatically raise HTTPException: HTTP_401_UNAUTHORIZED
)


@router.post('/signup', response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, user_service=Depends(get_user_service)):
    return await user_service.create_user(user_create)


@router.post('/login', response_model=Tokens, status_code=status.HTTP_200_OK)
async def login(user_data: UserLogin, user_service=Depends(get_user_service)):
    user = await user_service.authenticate_user(user_data.login, user_data.password)
    if not user:
        raise HTTPException(
            detail="Incorrect username or password",
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )

    subject = {"id": str(user.id), "role": "TODO:"}

    access_token = access_security.create_access_token(
        subject=subject,
        expires_delta=timedelta(minutes=settings.access_token_expires_min)
    )
    refresh_token = refresh_security.create_refresh_token(
        subject=subject,
        expires_delta=timedelta(days=settings.refresh_token_expires_days)
    )

    await user_service.create_or_update_token(user.id, refresh_token)

    return Tokens(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh")
async def refresh(
        request: Request,
        credentials: JwtAuthorizationCredentials = Security(refresh_security),
        user_service=Depends(get_user_service),
):
    bearer_token = request.headers['Authorization']
    refresh_token = bearer_token.split("Bearer ")[1]
    user_id = credentials.subject['id']

    if not await user_service.check_refresh_token(user_id, refresh_token):
        raise HTTPException(detail="Incorrect token", status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = access_security.create_access_token(subject=credentials.subject)
    refresh_token = refresh_security.create_refresh_token(
        subject=credentials.subject,
        expires_delta=timedelta(days=settings.refresh_token_expires_days)
    )

    return Tokens(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout")
async def logout(
        request: Request,
        credentials: JwtAuthorizationCredentials = Security(access_security),
        user_service=Depends(get_user_service),
):
    bearer_token = request.headers['Authorization']
    access_token = bearer_token.split("Bearer ")[1]
    user_id = credentials.subject['id']

    await user_service.invalidate_access_token(user_id, access_token)

    return JSONResponse(content={}, status_code=status.HTTP_200_OK)
