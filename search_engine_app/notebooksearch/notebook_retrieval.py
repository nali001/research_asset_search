# notebook_retrieval.py
'''' This module retrieves notebooks from Elasticsearch indexes
'''
import numpy as np
from spellchecker import SpellChecker
import requests
from bs4 import BeautifulSoup

from notebooksearch import utils
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.query import Match, MultiMatch

#-----------------------------------------------------------------------------------------------------------------------
def synonyms(term):
    response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
    soup = BeautifulSoup(response.text, 'html.parser')
    soup.find('section', {'class': 'css-191l5o0-ClassicContentCard e1qo4u830'})
    return [span.text for span in soup.findAll('a', {'class': 'css-1kg1yv8 eh475bn0'})]
#-----------------------------------------------------------------------------------------------------------------------

class NotebookRetriever():
    ''' Provide an entrypoint for generic notebook search
    '''
    def __init__(self, query_data, index_name): 
        self.query_data = query_data
        self.es = utils.create_es_client()
        self.index_name = index_name
        self.response_data = {}

    def retrieve_notebooks(self):
        ''' Retrieval notebooks from Elasticsearch
        '''
        es = self.es
        index_name = self.index_name 
        query_data = self.query_data
        query = query_data['query']
        page = int(query_data['page'])
        filter = query_data['filter']
        facets = query_data['facet']

        if query == "*" or query == "top10":
            query = ''
    
        location=(page-1)*10
        s = Search(using=es, index=index_name)
        # Construct query
        es_query = MultiMatch(query=query, fileds=["name", "description"], type="best_fields", minimum_should_match="50%")
        s.query(es_query)
        # Pagination (from: `location', size: 10)
        s = s[location:location+10]
        es_results = s.execute()
        
        # Extract notebooks from Elasticsearch responses
        es_notebooks=[]
        for search_result in es_results['hits']['hits']:
            es_notebooks.append(search_result['_source'])

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
            "results": es_notebooks,
            # "function_list": self.getAllfunctionList(request)
        }

        return results
