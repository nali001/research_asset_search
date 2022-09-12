from django.urls import path, include
from genericpages import views, models

urlpatterns = [
	#url(r'^index', views.index, name='index'),
    path('genericpages', views.genericpages, name='genericpages'),
    path('', views.landingpage, name='landingpage'),
]