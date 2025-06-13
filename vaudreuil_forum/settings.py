from dotenv import load_dotenv
load_dotenv()

import dj_database_url
import os
from pathlib import Path

# --- Base Directory ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security ---
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-dev-key")  # override in env vars
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# --- Installed Apps ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd-party
    'storages',  # for DigitalOcean Spaces

    # Local apps
    'accounts',
    'forum.apps.ForumConfig',

]

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # static files for prod
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- URL Configuration ---
ROOT_URLCONF = 'vaudreuil_forum.urls'

# --- Templates ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.global_announcements',
            ],
        },
    },
]

# --- WSGI Application ---
WSGI_APPLICATION = 'vaudreuil_forum.wsgi.application'

# --- Database ---
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        ssl_require=True,
    )
}



# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Static Files ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Media Files ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# If using DigitalOcean Spaces:
if os.getenv("USE_SPACES") == "True":
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None

# --- Default Primary Key ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Authentication ---
LOGIN_REDIRECT_URL = '/accounts/dashboard/'
LOGOUT_REDIRECT_URL = 'login'



# Use DATABASE_URL from environment if available
DATABASES['default'] = dj_database_url.config(
    default='sqlite:///db.sqlite3',
    conn_max_age=600,
    ssl_require=True
)

# Enable Whitenoise for static file handling
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
