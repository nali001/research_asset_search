''' Settings for deployment environment
'''
import os
from .settings_base import *
from pathlib import Path


host_ip = os.environ.get('HOST_IP')
postgres_hostname = os.environ.get('POSTGRES_HOSTNAME')
postgres_port = os.environ.get('POSTGRES_PORT')
postgres_db = os.environ.get('POSTGRES_DB')
postgres_user = os.environ.get('POSTGRES_USER')
postgres_password = os.environ.get('POSTGRES_PASSWORD')


# Allowed hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', host_ip]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#-------------------------- Uncomment STATICFILES_DIRS and comment STATIC_ROOT in development------------------
# The STATICFILES_DIRS tuple tells Django where to look for static files that are not tied to a particular app.
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Using the `collectstatic`` command, Django looks for all static files in your apps and collects them wherever you told it to, i.e. the STATIC_ROOT. 
# In our case, we are telling Django that when we run `python manage.py collectstatic`, gather all static files into a folder called staticfiles in our project root directory. 
# STATIC_ROOT = BASE_DIR / "static"
#---------------------------------------------------------------------------------------------------------------


#-------------------------- PostgreSQL database --------------------------
# from notebooksearch import postgres_tools
# # Create database `notebook_search` if not exists
# if not postgres_tools.database_exists("notebooksearch"): 
#     postgres_tools.create_databases(["notebooksearch"])

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'HOST': 'localhost',
#         'PORT': '5432',
#         'NAME': 'notebooksearch',
#         'USER': 'postgres',
#         'PASSWORD': 'notebooksearch2022',
#     }
# }
#---------------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': postgres_hostname,
        'PORT': postgres_port,
        'NAME': postgres_db,
        'USER': postgres_user,
        'PASSWORD': postgres_password,
    }
}