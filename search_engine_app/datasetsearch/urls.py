from django.urls import path
from datasetsearch import views
# from notebook_search import apis

urlpatterns = [
    path('dataset_search/', views.dataset_search_view, name='dataset_search'),
    # path('github_index_pipeline/', views.github_index_pipeline, name='github_index_pipeline'), 
    # path('api/', apis.welcome),
    # path('api/api_test/', apis.api_test),
]