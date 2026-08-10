"""
Django settings for boosternotes project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-g)(h61zja22%r+hx-l=x2jia$agp8_a+)+_p7nx7sb!r)b(f15'

# DEBUG defaults to off (Railway has no DEBUG env var, so production gets
# False automatically). DEBUG=True disables template caching and makes
# every SQL query keep a full traceback in memory for the life of the
# request — real, measurable overhead on every page. Export DEBUG=true
# locally if you want Django's debug error pages while developing.
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'boosternotes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        # APP_DIRS and 'loaders' are mutually exclusive — the cached loader
        # (which avoids re-reading + re-parsing every .html file from disk
        # on every render) has to be wired in manually via 'loaders' instead.
        'APP_DIRS': DEBUG,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'myapp.context_processors.global_settings',
            ],
            **({} if DEBUG else {
                'loaders': [
                    ('django.template.loaders.cached.Loader', [
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                    ]),
                ],
            }),
        },
    },
]

WSGI_APPLICATION = 'boosternotes.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            # WAL lets readers and a writer proceed concurrently instead of
            # the default rollback-journal mode where any writer blocks every
            # reader; timeout makes a second writer wait for the lock instead
            # of immediately raising "database is locked" (which, silently
            # caught by callers, was quietly failing background cache writes
            # — e.g. two Dropbox-link cache updates landing at the same time).
            'timeout': 20,
            'init_command': 'PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ── Upload size limits (100 MB) ───────────────────────────────────────────────
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600   # 100 MB in bytes
FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600   # 100 MB in bytes

# Auto-create the temp upload directory so Django's system check (files.E001)
# does not fail on Railway or any fresh deployment environment.
_TEMP_UPLOAD_DIR = os.path.join(BASE_DIR, 'tmp_uploads')
os.makedirs(_TEMP_UPLOAD_DIR, exist_ok=True)
FILE_UPLOAD_TEMP_DIR = _TEMP_UPLOAD_DIR

# ── Auth ──────────────────────────────────────────────────────────────────────
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# ── Caching ───────────────────────────────────────────────────────────────────
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'boosternotes-cache',
    }
}

# ── Razorpay (Test Mode) ──────────────────────────────────────────────────────
RAZORPAY_KEY_ID = 'rzp_live_TE9Wu5HGT8tqOs'
RAZORPAY_KEY_SECRET = '76hmR6Ptnol1qB9mGkMyhT9y'

# ── Dropbox ───────────────────────────────────────────────────────────────────
DROPBOX_APP_KEY       = "wgg2fsw5pf16x8q"
DROPBOX_APP_SECRET    = "38dg9gi6djz3zuu"
DROPBOX_REFRESH_TOKEN = "Si57f7yXuB0AAAAAAAAAAZGrsYbd1YLQpvGHxlJES4DRvKr7mDfZo8xqLaJBTY_s"
DROPBOX_FOLDER = '/elibrary'

CSRF_TRUSTED_ORIGINS = [
    "https://www.boosternotes.in",
    "https://boosternotes-production.up.railway.app",
    "https://www.ganeshsirclasses.online",
    
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
