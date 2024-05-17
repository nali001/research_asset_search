from django.urls import path
from apis import auth_api
from apis import notebook_search_api
from apis import notebook_download_api
from apis import context_search_api
from apis import relevancy_feedback_api


urlpatterns = [
    path('', auth_api.welcome_api, name='welcome'),
    path('initialize_app/', auth_api.initialize_app_api, name="initialize_app"),
    path('obtain_api_token/', auth_api.obatain_api_token_api, name="obtain_api_token"),
    path('create_userprofile/', notebook_search_api.create_userprofile_api, name='create_userprofile'),
    path('notebook_search/', notebook_search_api.notebook_search_api, name='notebook_search'),
    path('notebook_download/', notebook_download_api.notebook_download_api, name='notebook_download'),
    path('query_generation/', context_search_api.query_generation_api, name='query_generation'),
    path('context_search/', context_search_api.context_search_api, name='context_search'),
    path('relevancy_feedback/', relevancy_feedback_api.relevancy_feedback_api, name='relevancy_feedback'),
    path('test/', notebook_search_api.test, name='test'),
]