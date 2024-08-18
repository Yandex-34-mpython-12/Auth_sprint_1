from fastapi import APIRouter, Depends, Request
from src.core.config import settings
from src.schemas import OAuthUser
from src.services.oauth import CustomOauth, OAuthService, get_oauth_service

router = APIRouter(
    prefix=settings.api.v1.oauth,
    tags=["OAuth2"],
)

oauth2_scheme = CustomOauth(
    authorizationUrl=f"{settings.oauth.yandex_url}/authorize",
    tokenUrl=settings.api.oauth2_bearer_token_url
)


@router.post("/login")
async def login(request: Request, oauth_svc: OAuthService = Depends(get_oauth_service)):
    return await oauth_svc.authorize(request)


@router.get("/protected")
async def protected_route(user: OAuthUser = Depends(oauth2_scheme)):
    return {"user": user}
