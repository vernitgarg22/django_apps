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
from os import environ as env
import json

from django.core.exceptions import ImproperlyConfigured


DJANGO_HOME = env['DJANGO_HOME']
RUNNING_UNITTESTS = True if os.environ.get('RUNNING_UNITTESTS') == 'yes' else False

SECRETS_PATH = "/tests/test_secrets.json" if RUNNING_UNITTESTS else "/secrets.json"
with open(DJANGO_HOME + SECRETS_PATH) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets, default=None):
    try:
        return secrets[setting]
    except KeyError:              # pragma: no cover
        if default != None:
            secrets[setting] = default
            return secrets[setting]
        else:
            error_msg = "Set the environment variable '{0}'".format(setting)
            raise ImproperlyConfigured(error_msg)

def get_databases():
    tmp = get_secret('DATABASES')
    if tmp['default']['NAME'] == 'db.sqlite3':       # pragma: no cover
        tmp['default']['NAME'] = os.path.join(BASE_DIR, 'db.sqlite3')
    return tmp

MEDIA_ROOT = get_secret('MEDIA_SETTINGS')['MEDIA_ROOT']
MEDIA_URL = get_secret('MEDIA_SETTINGS')['MEDIA_URL']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = get_secret("SECRET_KEY")
DATABASES = get_databases()
DEBUG = get_secret('DEBUG', default=False)
DRY_RUN = get_secret('DRY_RUN', default=False)
ALLOWED_HOSTS = get_secret('ALLOWED_HOSTS', default=[])

CREDENTIALS = get_secret("CREDENTIALS")

AUTO_LOADED_DATA = {}
def load_auto_loaded_data():
    auto_names = get_secret('AUTO_LOADED_DATA_NAMES', default=[])
    for auto_name in auto_names:
        value = get_secret(auto_name)
        AUTO_LOADED_DATA[auto_name] = value

load_auto_loaded_data()

def add_vals_to_os():
    for key in [ "SLACK_API_TOKEN" ]:
        value = AUTO_LOADED_DATA[key]
        env[key] = value

add_vals_to_os()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# Monkey-patch stuff that we want disabled locally
if DEBUG:
    import tests.disabled
else:    # pragma: no cover

    # TODO review following settings for security
    # SESSION_COOKIE_SECURE = True
    # CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_REDIRECT_EXEMPT = [r'^(?!admin/).*']

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
    'car_info',
    'cod_utils',
    'data_cache',
    'dnninternet',
    'elections',
    'messenger',
    'photo_survey',
    'property_data',
    'waste_schedule',
    'waste_notifier',
    'waste_wizard',
    'weather_info',
    'corsheaders',
)
if RUNNING_UNITTESTS:
    INSTALLED_APPS = INSTALLED_APPS + ('tests',)

MIDDLEWARE = (
    # KARL: removing some of the sessions middleware package because assessments database has no sessions table
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

DATABASE_ROUTERS = [ 'django_apps.settings.DjangoAppsRouter', ]

class DjangoAppsRouter(object):
    """A router to control all database operations on models in
    the myapp2 application"""

    ModelDBMap = {
        "BSAPARCELDATA": "oashare",
        "bsaparceldata": "oashare",
        "DataSet": "data_cache",
        "DataCredential": "data_cache",
        "DataSource": "data_cache",
        "DataValue": "data_cache",
        "DataDescriptor": "data_cache",
        "DataCitySummary": "data_cache",
        "DTEActiveGasSite": "data_cache",
        "DNNKeyword": "data_cache",
        "Faqs": "dnninternet",
        "Htmltext": "dnninternet",
        "LicensePlateInfo": "license_plate_info",
        "Subscriber": "waste_collection",
        "ScheduleDetail": "waste_collection",
        "WasteItem": "waste_collection",
        "Sales": "eql",
        "ParcelMaster": "eql",
        "RoleType": "tidemark",
        "Parcel": "tidemark",
        "CaseType": "tidemark",
        "CaseMain": "tidemark",
        "Image": "photo_survey",
        "ImageMetadata": "photo_survey",
        "ParcelMetadata": "photo_survey",
        "PublicPropertyData": "photo_survey",

        # REVIEW put these somewhere else
        "MessengerClient": "default",
        "MessengerNotification": "default",
        "MessengerSubscriber": "default",

        "EscrowBalance": "property_data",
        "Sales": "eql",
        "Sketch": "eql",
        "Survey": "photo_survey",
        "Surveyor": "photo_survey",
        "SurveyorGroup": "photo_survey",
        "SurveyType": "photo_survey",
        "SurveyQuestion": "photo_survey",
        "SurveyAnswer": "photo_survey",
        "SurveyQuestionAvailAnswer": "photo_survey",
        "Tblztickets": "blight_tickets",
        "Whd01Parcl2017": "warehousedb",
        "MttTrackerExport2017": "finassessorprod",
        "MttTrackerExportTest": "finassessorprod",
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
        "Surveyor": "photo_survey_dev",
        "SurveyorGroup": "photo_survey_dev",
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
        if not RUNNING_UNITTESTS and db in [ 'blight_tickets', 'eql', 'tidemark' ]:    # pragma: no cover
            return False
        if model_name:
            return DjangoAppsRouter.get_db(model_name)
