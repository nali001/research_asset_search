# admin.py
from django.contrib import admin

# from notebook_search.models import BaseCellContent
# from notebook_search.models import BaseUserRequest
# from notebook_search.models import GithubNotebookResult
# from notebook_search.models import UserProfile
# from notebook_search.models import ContextSearchSession
# from notebook_search.models import NotebookSearchLog
# from notebook_search.models import NotebookSearchRequest
# from notebook_search.models import RelevancyFeedbackRequest

# from notebook_search.models import NotebookSearchRequestLog
# from notebook_search.models import ClientUser
from notebooksearch.models import UserProfile
# from notebook_search.models import NotebookSearchRequest
from notebooksearch.models import NotebookSearchLog
from notebooksearch.models import CellContent
from notebooksearch.models import QueryGenerationLog

# from notebook_search.models import KaggleNotebookResult





# python manage.py createsuperuser
# Username: admin
# Password: aubergine

# Register your models here then you browse through them on the admin interface. 
# This cane be updated in real time
# admin.site.register(GithubNotebookResult)
# admin.site.register(KaggleNotebookResult)
# admin.site.register(ContextSearchSession)
# admin.site.register(UserProfile)
# admin.site.register(NotebookSearchLog)
# admin.site.register(NotebookSearchRequest)
# admin.site.register(RelevancyFeedbackRequest)


# admin.site.register(NotebookSearchRequestLog)
# admin.site.register(ClientUser)
admin.site.register(UserProfile)
admin.site.register(NotebookSearchLog)
admin.site.register(CellContent)
admin.site.register(QueryGenerationLog)
# admin.site.register(KaggleNotebookResult)





