from os.path import join as os_path_join

# from WebNotes_config import ConfigData
from WebNotes_config import parse_configuration_file
# from pymongo import MongoClient

# config_parameters = {'django_pass': None,
#                      'django_language': 'en-us',
#                      'django_time_zone': 'UTC',
#                      'db_name': 'web_py_notes',
#                      'db_host': 'mongodb://127.0.0.1:27017',
#                      'db_port': None,
#                      'db_username': None,
#                      'db_password': None,
#                      'db_authSource': None,
#                      'db_authMechanism': None}

config_data = parse_configuration_file()

SECRET_KEY = config_data.get_django_password()

DEBUG = True  # DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'WebNotes.apps.WebnotesConfig',
    'WebNotes',
    'bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'WebPyNotes.urls'

templates_dir = config_data.get_templates_dir()

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [templates_dir, ],
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

WSGI_APPLICATION = 'WebPyNotes.wsgi.application'


# # DATABASES:
# mongo_client = MongoClient(config_data.get_database_client_host())
# mongo_db = mongo_client[config_data.get_database_name()]

# DATABASES = {
#        'default': {
#            'ENGINE': 'djongo',
#            'NAME': config_data.get_database_name(),
#            'CLIENT': {
#                'host': config_data.get_database_client_host(),
#                # 'port': config_data.get_database_client_port(),
#                # 'username': config_data.get_database_client_username(),
#                # 'password': config_data.get_database_client_password(),
#                # 'authSource': config_data.get_database_client_authSource(),
#                # 'authMechanism': config_data.get_database_client_authMechanism(),
#            }
#        }
#    }


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = config_data.get_django_language()

TIME_ZONE = config_data.get_django_time_zone()

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os_path_join(config_data.get_application_dir(), 'static'),
]

# File Storage
MEDIA_URL = '/user_database/'
MEDIA_ROOT = os_path_join(config_data.get_application_dir(), 'database')
# from os import mkdir as make_dir
# make_dir(MEDIA_ROOT)


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
