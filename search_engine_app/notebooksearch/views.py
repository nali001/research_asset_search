# notebook_search/views.py
# Only used for rendering HTML
import json
from django.shortcuts import render
from django.http import JsonResponse

from notebooksearch import notebook_retrieval
from ir import query_reformulation

from utils import utils
es = utils.create_es_client()

def notebook_search_view(request):
    ''' Retrieve notebooks from Elasticsearch and render the web page. 
    '''
    query_data = request.GET
    # print(query_data)
    index_name = "notebook_online"
    searcher = notebook_retrieval.NotebookRetriever(query_data, index_name)
    results = searcher.retrieve_notebooks()
    results["page_range"] = range(1, results["num_pages"])
    return render(request,'notebook_results.html', results)


def select_notebook_view(request):
    ''' Select one notebook. 
    '''
    if request.method == 'POST':
        query_data = json.loads(request.body.decode('utf-8'))
        print(query_data)

    query = query_data["query"]
    docid = query_data["docid"]
    index_name = "notebook_online"
    
    reformulator = query_reformulation.QueryReformulator(object_type='notebook', docid=docid, index_name=index_name)
    reformed = reformulator.reformulate_query_for_notebook(query=query)

    results = query_data.copy()
    results["reformed_query"] = reformed
    return JsonResponse(results, content_type='application/json')

def add_to_basket_view(request): 
    results = None
    return render(request,'notebook_results.html', results)
