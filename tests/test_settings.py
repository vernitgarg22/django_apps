"""
Django settings for django_apps project.

Generated by 'django-admin startproject' using Django 1.8.17.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import json

from django.core.exceptions import ImproperlyConfigured


# TODO move stuff that is shared between django_apps.settings and tests.test_settings into a shared location


DJANGO_HOME = os.environ['DJANGO_HOME']
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(DJANGO_HOME + "/tests/test_secrets.json") as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets, default=None):
    try:
        return secrets[setting]
    except KeyError:
        if default != None:
            secrets[setting] = default
            return secrets[setting]
        else:
            error_msg = "Set the {0} environment variable".format(setting)
            raise ImproperlyConfigured(error_msg)

def get_databases():
    tmp = get_secret('DATABASES')
    if tmp['default']['NAME'] == 'db.sqlite3':
        tmp['default']['NAME'] = os.path.join(BASE_DIR, 'db.sqlite3')
    return tmp

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = get_secret("SECRET_KEY")
DATABASES = get_databases()
DEBUG = get_secret('DEBUG', default=False)
ALLOWED_HOSTS = get_secret('ALLOWED_HOSTS', default=[])

AUTO_LOADED_DATA = {}
def load_auto_loaded_data():
    if AUTO_LOADED_DATA:
        return
    auto_names = get_secret('AUTO_LOADED_DATA_NAMES', default=[])
    for auto_name in auto_names:
        value = get_secret(auto_name)
        AUTO_LOADED_DATA[auto_name] = value

load_auto_loaded_data()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'assessments',
    'waste_schedule',
    'waste_notifier',
    'waste_wizard',
    'weather_info',
    'corsheaders',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
)

ROOT_URLCONF = 'django_apps.urls'

CORS_ORIGIN_ALLOW_ALL = True 

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'DIRS': [os.path.join(BASE_DIR, 'static')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_apps.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAdminUser',
    ],
    'PAGE_SIZE': 10
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True

APPEND_SLASH = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = DJANGO_HOME + "/static"
STATIC_URL = '/static/'

DATABASE_ROUTERS = [ 'tests.test_settings.DjangoAppsRouter', ]

class DjangoAppsRouter(object):
    """A router to control all database operations on models in
    the myapp2 application"""

    ModelDBMap = {
        "Subscriber": "waste_collection",
        "ScheduleDetail": "waste_collection",
        "WasteItem": "waste_collection",
    }

    @staticmethod
    def get_db(model):
        name = model.__name__
        return DjangoAppsRouter.ModelDBMap[name] if DjangoAppsRouter.ModelDBMap.get(name) else None

    def db_for_read(self, model, **hints):
        return DjangoAppsRouter.get_db(model)

    def db_for_write(self, model, **hints):
        return DjangoAppsRouter.get_db(model)

    def allow_relation(self, obj1, obj2, **hints):
        return DjangoAppsRouter.get_db(model)

    def allow_migrate(self, db, model):
        return DjangoAppsRouter.get_db(model)
