# notebook_search/views.py
# Only used for rendering HTML
from django.shortcuts import render

from notebooksearch import notebook_retrieval
from notebooksearch import genericsearch

from utils import utils
es = utils.create_es_client()


import json

def notebook_search_view(request):
    ''' Retrieve notebooks from Elasticsearch and render the web page. 
    '''
    query_data = request.GET
    print(query_data)
    index_name = "notebook_online"
    searcher = notebook_retrieval.NotebookRetriever(query_data, index_name)
    results = searcher.retrieve_notebooks()
    # searcher = genericsearch.Genericsearch(request, es, index_name)
    # results = searcher.genericsearch()
    results["page_range"] = range(1, results["num_pages"])

    # with open("results_hhhhhhh.json", "w") as outfile:
    #     json.dump(results, outfile)

    print(type(results))
    return render(request,'notebook_results.html', results)
 