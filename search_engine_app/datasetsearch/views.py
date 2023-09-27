# dataset_search/views.py
# Only used for rendering HTML
from django.shortcuts import render

from datasetsearch import dataset_retrieval

def dataset_search_view(request):
    ''' Retrieve datasets from Elasticsearch and render the web page. 
    '''
    query_data = request.GET
    print(query_data)
    index_name = "dataset_online"
    searcher = dataset_retrieval.DatasetRetriever(query_data, index_name)
    results = searcher.retrieve_datasets()

    results["page_range"] = range(1, results["num_pages"])
    
    # results = {
    #     'endpoint': '../../datasetsearch/dataset_search', 
    #     'query': 'climate change', 
    #     'html_url': 'Link to HTML',
    #     'name': 'Name of the item',
    #     'description': 'Description of the item',
    #     'source': 'Source code or origin'
    #     }

    return render(request,'dataset_results.html', results)
 