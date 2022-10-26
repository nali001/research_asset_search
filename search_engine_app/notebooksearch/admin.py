# admin.py
from django.contrib import admin

from notebooksearch.models import UserProfile
from notebooksearch.models import NotebookSearchLog
from notebooksearch.models import CellContent
from notebooksearch.models import GeneratedQuery
from notebooksearch.models import QueryGenerationLog
from notebooksearch.models import ContextSearchLog
from notebooksearch.models import AnnotatedNotebook
from notebooksearch.models import RelevancyFeedbackLog


# python manage.py createsuperuser
# Username: admin
# Password: aubergine

admin.site.register(UserProfile)
admin.site.register(NotebookSearchLog)
admin.site.register(CellContent)
admin.site.register(QueryGenerationLog)
admin.site.register(GeneratedQuery)
admin.site.register(ContextSearchLog)
admin.site.register(AnnotatedNotebook)
admin.site.register(RelevancyFeedbackLog)







