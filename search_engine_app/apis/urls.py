from django.urls import path
from apis import auth_api
from apis import notebook_search_api
from apis import context_search_api


# from notebook_search import apis

urlpatterns = [
    path('', auth_api.welcome_api, name='welcome'),
    path('initialize_app/', auth_api.initialize_app_api, name="initialize_app"),
    path('obtain_api_token/', auth_api.obatain_api_token_api, name="obtain_api_token"),
    # path('relevancy_feedback/', notebook_search_api.relevancy_feedback, name='relevancy_feedback'),
    path('create_userprofile/', notebook_search_api.create_userprofile_api, name='create_userprofile'),
    path('notebook_search/', notebook_search_api.notebook_search_api, name='notebook_search'),
    path('query_generation/', context_search_api.query_generation_api, name='query_generation'),
    path('context_search/', context_search_api.context_search_api, name='context_search'),
    path('test/', notebook_search_api.test, name='test'),
]