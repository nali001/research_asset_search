# dataset_search/views.py
# Only used for rendering HTML
import os
from dotenv import load_dotenv

import json
from django.shortcuts import render
from django.http import JsonResponse

from datasetsearch import dataset_retrieval
from ir import query_reformulation


def dataset_search_view(request):
    ''' Retrieve datasets from Elasticsearch and render the web page. 
    '''
    query_data = request.GET
    # print(query_data)

    # Load environment variables from .env file
    load_dotenv()

    index_name_list = os.getenv("ES_DATASET_INDEX_NAMES", "").split(",")

    searcher = dataset_retrieval.DatasetRetriever(query_data, index_name_list)
    results = searcher.retrieve_datasets()

    results["page_range"] = range(1, results["num_pages"])
    
    return render(request,'dataset_results.html', results)


def select_dataset_view(request):
    ''' Select one dataset. 
    '''
    load_dotenv()

    index_name_list = os.getenv("ES_DATASET_INDEX_NAMES", "").split(",")
    
    if request.method == 'POST':
        query_data = json.loads(request.body.decode('utf-8'))
        print(query_data)

    query = query_data["query"]
    docid = query_data["docid"]
    
    
    reformulator = query_reformulation.QueryReformulator(object_type='dataset', docid=docid, index_name_list=index_name_list)
    reformed = reformulator.reformulate_query_for_notebook(query=query)

    results = query_data.copy()
    results["reformed_query"] = reformed
    return JsonResponse(results, content_type='application/json')

def add_to_basket_view(request): 
    results = None
    return render(request,'dataset_results.html', results)
