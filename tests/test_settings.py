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
    except KeyError:              # pragma: no cover
        if default != None:
            secrets[setting] = default
            return secrets[setting]
        else:
            error_msg = "Set the {0} environment variable".format(setting)
            raise ImproperlyConfigured(error_msg)

def get_databases():
    tmp = get_secret('DATABASES')
    if tmp['default']['NAME'] == 'db.sqlite3':       # pragma: no cover
        tmp['default']['NAME'] = os.path.join(BASE_DIR, 'db.sqlite3')
    return tmp

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = get_secret("SECRET_KEY")
DATABASES = get_databases()
DEBUG = get_secret('DEBUG', default=False)
DRY_RUN = get_secret('DRY_RUN', default=False)
ALLOWED_HOSTS = get_secret('ALLOWED_HOSTS', default=[])

AUTO_LOADED_DATA = {}
def load_auto_loaded_data():
    if AUTO_LOADED_DATA:    # pragma: no cover
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
    'rest_framework.authtoken',
    'assessments',
    'assessors_data',
    'blight_tickets',
    'photo_survey',
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

RUNNING_UNITTESTS = True

DATABASE_ROUTERS = [ 'tests.test_settings.DjangoAppsRouter', ]

class DjangoAppsRouter(object):
    """A router to control all database operations on models in
    the myapp2 application"""

    ModelDBMap = {
        "Subscriber": "waste_collection",
        "ScheduleDetail": "waste_collection",
        "WasteItem": "waste_collection",
        "Sales": "eql",
        "RoleType": "tidemark",
        "Parcel": "tidemark",
        "CaseType": "tidemark",
        "CaseMain": "tidemark",
        "Image": "photo_survey",
        "ImageMetadata": "photo_survey",
        "ParcelMetadata": "photo_survey",
        "PublicPropertyData": "photo_survey",
        "Survey": "photo_survey",
        "SurveyType": "photo_survey",
        "SurveyQuestion": "photo_survey",
        "SurveyAnswer": "photo_survey",
        "SurveyQuestionAvailAnswer": "photo_survey",
        "Tblztickets": "blight_tickets",
        "Whd01Parcl2017": "assessors_data",
    }

    ModelDBMapDev = {
        "Subscriber": "waste_collection_dev",
        "ScheduleDetail": "waste_collection_dev",
        "WasteItem": "waste_collection_dev",
        "Image": "photo_survey_dev",
        "ImageMetadata": "photo_survey_dev",
        "ParcelMetadata": "photo_survey_dev",
        "PublicPropertyData": "photo_survey_dev",
        "Survey": "photo_survey_dev",
        "SurveyType": "photo_survey_dev",
        "SurveyQuestion": "photo_survey_dev",
        "SurveyAnswer": "photo_survey_dev",
        "SurveyQuestionAvailAnswer": "photo_survey_dev",
    }

    @staticmethod
    def get_db(model):
        name = model if type(model) == str else model.__name__
        database = None
        if DEBUG:               # pragma: no cover
            database = DjangoAppsRouter.ModelDBMapDev.get(name)
        if not database:
            database = DjangoAppsRouter.ModelDBMap.get(name)
        return database

    def db_for_read(self, model, **hints):
        return DjangoAppsRouter.get_db(model)

    def db_for_write(self, model, **hints):
        return DjangoAppsRouter.get_db(model)

    def allow_relation(self, obj1, obj2, **hints):
        # TODO always return True?
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name:
            return DjangoAppsRouter.get_db(model_name)
