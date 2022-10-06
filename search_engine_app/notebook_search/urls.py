from django.urls import path
from notebook_search import views
# from notebook_search import apis

urlpatterns = [
    path('genericsearch/', views.genericsearch_view, name='genericsearch'),
    # path('github_index_pipeline/', views.github_index_pipeline, name='github_index_pipeline'), 
    # path('api/', apis.welcome),
    # path('api/api_test/', apis.api_test),
]