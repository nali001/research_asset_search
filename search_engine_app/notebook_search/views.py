from django.shortcuts import render
from django.http import HttpResponse
from . import rankings
from .models import Movie



def index(request): 
    result = {'result': 'Haha'}
    return render(request, 'index.html', result)

def search_result(request):
    context_list = [1, 2, 3]

    # Generate htmls using new data
    return render(request, 'search_result.html', {'context_list': context_list})

def ui_test(request):
    context = rankings.elastic_test()
    return render(request, 'test.html', {'context': context})

from django.shortcuts import render

def movies(request):
	movies = Movie.objects.all() #queryset containing all movies we just created
	return render(request=request, template_name="movies.html", context={'movies':movies})

