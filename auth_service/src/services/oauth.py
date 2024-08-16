from functools import lru_cache
from urllib.parse import parse_qs

from fastapi import Depends, Request, HTTPException, status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.db.postgres import db_helper


class OAuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def authorize(self, request: Request) -> dict[str, str]:
        data = await request.body()
        parsed_data = {k: v[0] for k, v in parse_qs(data.decode()).items()}
        if 'code' in parsed_data:
            url = f'{settings.oauth.yandex_url}/token'
            data = {
                "grant_type": "authorization_code",
                "code": parsed_data['code'],
                "client_id": settings.oauth.client_id,
                "client_secret": settings.oauth.client_secret,
            }
            res = await self.send_request(url, data)
            return {"access_token": res['access_token']}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    async def send_request(self, url: str, data: dict[str, str]) -> dict:
        async with AsyncClient() as client:
            response = await client.post(url, data=data)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                )
            return response.json()


@lru_cache()
def get_oauth_service(
    db: AsyncSession = Depends(db_helper.session_getter),
) -> OAuthService:
    return OAuthService(db=db)
