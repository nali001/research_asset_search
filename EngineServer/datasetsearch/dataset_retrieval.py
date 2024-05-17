# dataset_retrieval.py
'''' This module retrieves datasets from Elasticsearch indexes
'''
import numpy as np
# from spellchecker import SpellChecker
import requests
from bs4 import BeautifulSoup

from utils import utils
# from indexer import dataset_indexing

#-----------------------------------------------------------------------------------------------------------------------
def synonyms(term):
    response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
    soup = BeautifulSoup(response.text, 'html.parser')
    soup.find('section', {'class': 'css-191l5o0-ClassicContentCard e1qo4u830'})
    return [span.text for span in soup.findAll('a', {'class': 'css-1kg1yv8 eh475bn0'})]
#-----------------------------------------------------------------------------------------------------------------------

class DatasetRetriever():
    ''' Provide an entrypoint for generic dataset search
    '''
    def __init__(self, query_data, index_name_list): 
        self.query_data = query_data
        self.es = utils.create_es_client()
        self.index_name_list = index_name_list
        self.response_data = {}


    def retrieve_datasets(self):
        ''' Retrieval datasets from Elasticsearch
        '''
        es = self.es
        index_name_list = self.index_name_list 
        query_data = self.query_data
        # Index the datasets if there is no indexes before. 
        # dataset_indexing.index_kaggle_notebooks()

        query = query_data['query']
        page = int(query_data['page'])
        filter = query_data['filter']
        facets = query_data['facet']

        if query == "*" or query == "top10":
            query = ''
        location=(page-1)*10
        if query=="*" or query=="top10":
            query_body={
                    "from" : location,
                    "size" : 10,
                    "query": {
                        "bool" : {
                            "must" : {
                                "match_all": {}
                            }
                        }
                    }
                }
        else:
            # user_request = "some_param"
            query_body = {
                "from" : location,
                "size" : 10,
                "query": {
                    "bool": {
                        "must": {
                            "multi_match" : {
                                "query": query,
                                "fields": [ "name", "description"],
                                # "type": "best_fields",
                                # "minimum_should_match": "50%"
                            }
                        },
                    }
                }
            }

        es_results = es.search(index=index_name_list, body=query_body)
        # Extract datasets from Elasticsearch responses
        # The responses from Elasticsearch are not original dataset contents, 
        # but rather processed information.  
        es_datasets=[]
        for search_result in es_results['hits']['hits']:
            one_dataset = search_result['_source']

            es_datasets.append(one_dataset)
        num_hits=es_results['hits']['total']['value']
        num_pages=round(np.ceil(num_hits/10)+1)
        # Only display the first 11 pages
        if(num_pages>10):
            num_pages = 11
        facets=[]
        results={
            "query": query,
            "facets": facets,
            "num_hits": num_hits,
            "num_pages": num_pages,
            "current_page": page,
            "results": es_datasets
            # "function_list": self.getAllfunctionList(request)
        }
        # Returned results will be serialized by DatasetSearchResultSerializer
        return results
