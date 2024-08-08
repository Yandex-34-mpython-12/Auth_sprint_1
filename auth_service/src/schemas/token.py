from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class Tokens(AccessToken, RefreshToken):
    pass
