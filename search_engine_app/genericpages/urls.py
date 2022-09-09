from django.urls import path, include
from genericpages import views, models
from django.conf.urls.static import static

urlpatterns = [
	#url(r'^index', views.index, name='index'),
    path(r'^genericpages', views.genericpages, name='genericpages'),
    path('', views.landingpage, name='landingpage'),
]