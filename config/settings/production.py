from .base import *

STATICFILES_DIRS = [
  str(ROOT_DIR.path('assets')),
]

WEBPACK_LOADER = {
  'DEFAULT': {
    'BUNDLE_DIR_NAME': 'bundles/',
    'STATS_FILE': str(ROOT_DIR.path('webpack-stats.prod.json')),
  }
}

DEBUG = True

# ALLOWED_HOSTS = ['annotate.vframe.io']
USE_X_FORWARDED_HOST = True
ALLOWED_HOSTS = ['annotate.vframe.io', 'fax.vframe.io', 'localhost', '127.0.0.1', '[::1]']
CSRF_TRUSTED_ORIGINS = ['annotate.vframe.io', 'fax.vframe.io', 'localhost', '128.0.0.1', '[::1]']

CSRF_COOKIE_SECURE = True

SECRET_KEY = env('DJANGO_SECRET_KEY', default='replace123with:456env789var')



DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': str(ROOT_DIR.path('db.sqlite3')),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASS'),
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}
