''' Settings for deployment environment
'''

from .settings_base import *
from pathlib import Path


postgres_hostname = os.environ.get('POSTGRES_HOSTNAME')
postgres_port = os.environ.get('POSTGRES_PORT')
postgres_db = os.environ.get('POSTGRES_DB')
postgres_user = os.environ.get('POSTGRES_USER')
postgres_password = os.environ.get('POSTGRES_PASSWORD')



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# replace the following line with your actual IP address
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'IP_address']

#-------------------------- Uncomment STATICFILES_DIRS and comment STATIC_ROOT in development------------------
# The STATICFILES_DIRS tuple tells Django where to look for static files that are not tied to a particular app.
# STATICFILES_DIRS = [
#     BASE_DIR / "static",
# ]

# Using the `collectstatic`` command, Django looks for all static files in your apps and collects them wherever you told it to, i.e. the STATIC_ROOT. 
# In our case, we are telling Django that when we run `python manage.py collectstatic`, gather all static files into a folder called staticfiles in our project root directory. 
STATIC_ROOT = BASE_DIR / "static"
#---------------------------------------------------------------------------------------------------------------

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

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '']
