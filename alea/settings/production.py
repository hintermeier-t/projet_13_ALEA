"""
    Django production settings for ALEA.
"""
import os
from . import *

ALLOWED_HOSTS = ['46.101.80.206']
DEBUG = False

SECRET_KEY = '33Pjch5kFbxc7PifA0Xrapo8whksOJYWwtcOduYAEOls1lua05g5DvXeqVitayRhkuz7+izozq+i eDezBUu1tqTkzbJdUg=='

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "alea",
        "USER": "thomadmin",
        "PASSWORD": "2s7gix9u",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
