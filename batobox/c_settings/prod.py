from batobox.settings import *

SECRET_KEY = env('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*', 'localhost', 'batobox.net', 'api.batobox.net']

CSRF_TRUSTED_ORIGINS = ['https://batobox.net', 'https://api.batobox.net']

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}

DATABASES['log_db'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'log_db.sqlite3',
}

# DATABASES['default'] = {
#     'ENGINE': 'django.db.backends.postgresql_psycopg2',
#     'NAME': 'batobox_central_db',
#     'USER': 'batobox_central_db_admin',
#     'PASSWORD': 'ojf$655%%4edrf@cfrf',
#     'HOST': 'localhost',
#     'PORT': '',
# }
#
# DATABASES['log_db'] = {
#     'ENGINE': 'django.db.backends.postgresql_psycopg2',
#     'NAME': 'batobox_log_db',
#     'USER': 'batobox_central_db_admin',
#     'PASSWORD': 'ojf$655%%4edrf@cfrf',
#     'HOST': 'localhost',
#     'PORT': '',
# }
