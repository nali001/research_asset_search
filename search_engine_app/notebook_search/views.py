# notebook_search/views.py
# Only used for rendering HTML
from django.shortcuts import render

import urllib
import json
import numpy as np
import requests
from bs4 import BeautifulSoup
from spellchecker import SpellChecker

import os

from notebook_search import utils
# from notebook_search import notebook_retrieval
from notebook_search import genericsearch



# Create Elasticsearch client
es = utils.create_es_client()

def genericsearch_view(request):
    ''' Retrieve notebooks from Elasticsearch and render the web page. 
    '''
    index_name = "kaggle_notebooks"
    searcher = genericsearch.Genericsearch(request, es, index_name)
    results = searcher.genericsearch()
    return render(request,'notebook_results.html', results)
