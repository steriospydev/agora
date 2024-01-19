from .base import *

DEBUG = env('DEBUG')
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
INSTALLED_APPS.append('debug_toolbar')
INSTALLED_APPS.append('import_export')
MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
INTERNAL_IPS = ["127.0.0.1",]

#  Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

