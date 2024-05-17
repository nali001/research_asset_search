''' Settings for deployment environment
'''
import os
from .settings_base import *

# The variables are stored in `.env` file under the same dir as this file
host_ip = os.environ.get('HOST_IP')
postgres_hostname = os.environ.get('POSTGRES_HOSTNAME')
postgres_port = os.environ.get('POSTGRES_PORT')
postgres_db = os.environ.get('POSTGRES_DB')
postgres_user = os.environ.get('POSTGRES_USER')
postgres_password = os.environ.get('POSTGRES_PASSWORD')


# Allowed hosts
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', host_ip]
# ALLOWED_HOSTS = ['145.100.135.19']
ALLOWED_HOSTS = ['*']

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
#---------------------------------------------------------------------------

#-------------------------- URL settings --------------------------
# APPEND_SLASH=False
#-------------------------------------------------------------------
