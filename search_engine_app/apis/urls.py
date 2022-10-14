from django.urls import path
from apis import notebook_search_api
# from notebook_search import apis

urlpatterns = [
    path('', notebook_search_api.welcome, name='welcome'),
    path('database_test/', notebook_search_api.database_test, name='database_test'),
    # path('notebook_search/', notebook_search_api, name='notebook_search_api'),
    path('notebook_search/', notebook_search_api.notebook_search, name='notebook_search'),
    path('context_search/', notebook_search_api.context_search, name='context_search'),
    path('query_generation/', notebook_search_api.query_generation, name='query_generation'),
    path('relevancy_feedback/', notebook_search_api.relevancy_feedback, name='relevancy_feedback'),
]