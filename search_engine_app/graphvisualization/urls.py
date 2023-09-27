from django.urls import path
from graphvisualization import views
# from notebook_search import apis

urlpatterns = [
    path('graph_visualization/', views.graph_visualization_view, name='graph_visualization'),
    # path('github_index_pipeline/', views.github_index_pipeline, name='github_index_pipeline'), 
    # path('api/', apis.welcome),
    # path('api/api_test/', apis.api_test),
]