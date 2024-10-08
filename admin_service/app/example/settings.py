import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

DEBUG = os.environ.get('DEBUG', False) == 'True'

include(
    'components/database.py',
    'components/installed_apps.py',
    'components/middleware.py',
    'components/templates.py',
)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(', ')

INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'example.urls'

WSGI_APPLICATION = 'example.wsgi.application'


AUTH_USER_MODEL = "custom_user.User"

AUTH_API_LOGIN_URL = os.environ.get("AUTH_API_LOGIN_URL")

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'custom_user.backend.CustomBackend',
]

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR.parent, 'data/static')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
