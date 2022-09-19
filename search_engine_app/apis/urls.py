from django.urls import path
from apis import notebook_search_api
# from notebook_search import apis

urlpatterns = [
    path('', notebook_search_api.welcome, name='welcome'),
    # path('notebook_search/', notebook_search_api, name='notebook_search_api'),
    path('notebook_search/', notebook_search_api.notebook_search, name='notebook_search'),
]