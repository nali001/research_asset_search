from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(f'test', views.ui_test, name='ui_test'),
    path(f'result', views.search_result, name='result'),
    path(f'movies', views.movies, name='movies'),
]