''' Settings for deployment environment
'''

from .settings_base import *
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# from notebook_search import postgres_tools
# postgres_tools.create_databases(["notebook_search"])

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'HOST': 'localhost',
#         'PORT': '5432',
#         'NAME': 'notebook_search',
#         'USER': 'postgres',
#         'PASSWORD': 'aubergine',
#     }
# }

#-------------------------- Uncomment STATICFILES_DIRS and comment STATIC_ROOT in development------------------
# The STATICFILES_DIRS tuple tells Django where to look for static files that are not tied to a particular app.
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Using the `collectstatic`` command, Django looks for all static files in your apps and collects them wherever you told it to, i.e. the STATIC_ROOT. 
# In our case, we are telling Django that when we run `python manage.py collectstatic`, gather all static files into a folder called staticfiles in our project root directory. 
# STATIC_ROOT = BASE_DIR / "static"
#---------------------------------------------------------------------------------------------------------------
