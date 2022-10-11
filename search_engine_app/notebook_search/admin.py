from django.contrib import admin
from notebook_search.models import GithubNotebookResult, KaggleNotebookResult

# python manage.py createsuperuser
# Username: admin
# Password: aubergine


# Register your models here.
admin.site.register(GithubNotebookResult)
admin.site.register(KaggleNotebookResult)


