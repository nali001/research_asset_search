# dataset_search/views.py
# Only used for rendering HTML
from django.shortcuts import render

# from notebooksearch import notebook_retrieval
# from notebooksearch import genericsearch

# from notebooksearch import utils
# es = utils.create_es_client()

def dataset_search_view(request):
    ''' Retrieve notebooks from Elasticsearch and render the web page. 
    '''
    # query_data = request.GET
    # print(query_data)
    # index_name = "kaggle_online"
    # searcher = notebook_retrieval.NotebookRetriever(query_data, index_name)
    # results = searcher.retrieve_notebooks()
    # searcher = genericsearch.Genericsearch(request, es, index_name)
    # results = searcher.genericsearch()
    # results["page_range"] = range(1, results["num_pages"])
    results = {
        'endpoint': '../../datasetsearch/dataset_search', 
        'query': 'climate change', 
        'html_url': 'Link to HTML',
        'name': 'Name of the item',
        'description': 'Description of the item',
        'source': 'Source code or origin'
        }

    return render(request,'dataset_results.html', results)
 