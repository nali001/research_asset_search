''' Settings for deployment environment
This will be overwritten by settings_prod.py when deploy 
through django_app_setup.sh specified in Dockerfile
'''
from .settings_dev import *
