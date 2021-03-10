"""
    Django production settings for ALEA.
"""
import os

ALLOWED_HOSTS = ["46.101.80.206"]
DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "alea",
        "USER": "thomas",
        "PASSWORD": "2s7gix9u",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
