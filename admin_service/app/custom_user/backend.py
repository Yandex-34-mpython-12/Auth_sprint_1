import http
from enum import Enum

import jwt
import requests
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class Roles(Enum):
    ADMIN = "ADMIN"
    SUBSCRIBER = "SUBSCRIBER"


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        url = settings.AUTH_API_LOGIN_URL
        payload = {'username': username, 'password': password}
        response = requests.post(url, data=payload)
        if response.status_code != http.HTTPStatus.OK:
            return None

        try:
            res = response.json()
            data = jwt.decode(
                res['access_token'], settings.JWT_SECRET_KEY,
                audience="fastapi-users:auth",
                algorithms=[settings.JWT_ALGORITHM]
            )
        except Exception:
            return None

        try:
            user, created = User.objects.get_or_create(id=data['sub'], )
            user.email = data.get('email')
            user.is_admin = data.get('role') == Roles.ADMIN
            user.is_active = data.get('is_active')
            user.save()
        except Exception as e:
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
