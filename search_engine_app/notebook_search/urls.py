from django.urls import path, include
from notebook_search import views, models

urlpatterns = [
    path('genericsearch/', views.genericsearch, name='genericsearch'),
    path('github_index_pipeline/', views.github_index_pipeline, name='github_index_pipeline')
]

