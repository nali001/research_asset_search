''' Basic settings for bothe development and deployment environment
'''
from pathlib import Path
import os
from turtle import pos

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@i7f150h^z1f9wiq7541i)h_^8$4a!zoe+fb+050y6f7xfq2ev'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# # replace the following line with your actual IP address
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'IP_address']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'search_engine_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'search_engine_app.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



#-------------------------- Installed apps ------------------------
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'genericpages',
    'notebook_search', 
    'django_elasticsearch_dsl', 
    'apis', 
    'rest_framework', 
    'rest_framework.authtoken', 
]

#------------------------------------------------------------------


#-------------------------- Static files  ------------------------
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = "static/"

#------------------------------------------------------------------



#-------------------------- PostgreSQL database --------------------------
from notebook_search import postgres_tools
# Create database `notebook_search` if not exists
if not postgres_tools.database_exists("notebook_search"): 
    postgres_tools.create_databases(["notebook_search"])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'PORT': '5432',
        'NAME': 'notebook_search',
        'USER': 'postgres',
        'PASSWORD': 'notebooksearch2022',
    }
}
#---------------------------------------------------------------------------


#-------------------------- Elasticsearch database -------------------------
from elasticsearch import Elasticsearch
ELASTICSEARCH_HOSTNAMES = ["elasticsearch", "localhost"]
valid_hostname = None
for host in ELASTICSEARCH_HOSTNAMES: 
    es = Elasticsearch(
        hosts=[{"host": host, "port": 9200}],
        http_auth=["elastic", "changeme"],
        )
    if es.ping(): 
        valid_hostname = host
        break

if valid_hostname == None: 
    raise Exception('Please start Elasticsearch service first!')

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': os.getenv("ELASTICSEARCH_DSL_HOSTS", valid_hostname + ':9200')
    },
}
print('VALIDDDDDDDDDDDDDDD Elasticsearch hostname:', valid_hostname)
#----------------------------------------------------------------------------------------



#-------------------------------- Django REST API --------------------------------
DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
)

if DEBUG:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES, 
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
#------------------------------------------------------------------------------------
