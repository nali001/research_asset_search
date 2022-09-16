from django.urls import path, include
from genericpages import views, models

urlpatterns = [
	#url(r'^index', views.index, name='index'),
    path('', views.landingpage, name='landingpage'),
    path('genericpages', views.genericpages, name='genericpages'),
    path('ui_test', views.ui_test, name='ui_test'),
]