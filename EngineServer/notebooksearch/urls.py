from django.urls import path
from notebooksearch import views
# from notebook_search import apis

urlpatterns = [
    path('notebook_search/', views.notebook_search_view, name='notebook_search'),
    path('select_notebook/', views.select_notebook_view, name='select_notebook'),
    path('add_to_basket/', views.add_to_basket_view, name='add_to_basket'),
    # path('github_index_pipeline/', views.github_index_pipeline, name='github_index_pipeline'), 
    # path('api/', apis.welcome),
    # path('api/api_test/', apis.api_test),
]