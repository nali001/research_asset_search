# notebook_search/views.py
# Only used for rendering HTML
from django.shortcuts import render
# from notebook_search import utils
from notebooksearch import notebook_retrieval
# from notebook_search import genericsearch


def notebook_search_view(request):
    ''' Retrieve notebooks from Elasticsearch and render the web page. 
    '''
    query_data = request.GET
    print(query_data)
    index_name = "kaggle_notebooks"
    searcher = notebook_retrieval.NotebookRetriever(query_data, index_name)
    results = searcher.retrieve_notebooks()
    return render(request,'notebook_results.html', results)
