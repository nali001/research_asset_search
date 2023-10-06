from elasticsearch_dsl import Index
import json
import os
import time

import pandas as pd
import datetime

from utils import utils
# from notebooksearch import notebook_retrieval
from elasticsearch import Elasticsearch

from .indexing_schema import DATASET_INDEX_SUMMARY

# ----------------------------------------------------------------------------------

class ElasticsearchIndexer():
    '''Index preprocessed notebooks with Elasticsearch. 

    Attrs: 
        - es: Elasticsearch client
        - index_name: Elasticsearch index name. 
        - input_path: The path for storing notebook files. 
        - source_name: 'Kaggle' or 'Github'. The repository source for notebooks
        - doc_type: 'preprocessed' or 'raw'. The document type for notebooks
    '''
    def __init__(self, es: Elasticsearch, source_name: str, doc_type:str, index_name:str, input_path:str): 
        self.es = es
        self.index_name = index_name
        self.input_path = input_path
        self.source_name = source_name
        self.doc_type = doc_type
        # self.source_file_name = source_file_name
    

    def index_datasets(self, reindex = False): 
        ''' Index generated files into Elasticsearch database given index name
        
        Can index raw notebooks and preprocessed notebooks. 

        When indexing raw notebooks, it requires a `kaggle_raw_notebooks.csv` file placed under `notebook_path`
        '''
        index_name = self.index_name
        es = self.es
        index = Index(index_name, es)
        if reindex: 
            index.delete(ignore=[400, 404])
        if es.indices.exists(index = index_name): 
            print(f'\n{index_name} already exists!\n')
            return True
        else: 
            index.settings(
                index={'mapping': {'ignore_malformed': True}}
            )
            index.create()

            # Call Elasticsearch to index the files
            if self.doc_type == 'preprocessed': 
                root = self.input_path
                count = 0
                for path, _, files in os.walk(root):
                    for name in files:
                        indexfile= os.path.join(path, name)
                        index_content = utils.read_json_file(indexfile)
                        newRecord = {}
                        newRecord['id'] = index_content["html_url"]
                        for key in DATASET_INDEX_SUMMARY.keys():
                            newRecord[key] = index_content[key]
                # for count, record in enumerate(indexfiles): 
                        try: 
                            res = es.index(index=index_name, id = newRecord["id"], document=newRecord)
                            print(f'Indexing {str(count+1)}-th record!\n')
                            count = count + 1
                        except Exception as e: 
                            print(e, "\n")
                            print(newRecord["name"])
                es.indices.refresh(index=index_name)
            else: 
                pass
        return True
# ----------------------------------------------------------------------------------

# ================= Below are the functions to generate different indexes =======================
# Depending on the content you want to include in the Elasticsearch index database. 

def index_datasets(data_dir, source_name=None, query_source=None, preprocess_type=None, reindex=False):  
    ''' Index preprocessed datasets, 
    this will further retrieved by Elasticsearch
    '''       
    # Try to reconnect to Elasticsearch for 10 times when failing
    # This 
    for i in range(100): 
        es = utils.create_es_client()
        if es == None: 
            time.sleep(0.5)
            continue
        else: 
            break

    # Index datasets crawled from various repositories
    input_path = f'{data_dir}/{source_name}/preprocessed_{preprocess_type}/{query_source}/'
    
    # Use date to mark the index generation time
    current_date = str(datetime.date.today())
    index_name = f"{source_name.lower()}_datasets_{current_date}"
    print(f'Input path: {input_path}')
    print(f'Index name: {index_name}')

    indexer = ElasticsearchIndexer(
        es=es, 
        source_name=source_name, 
        doc_type="preprocessed", 
        index_name=index_name, 
        input_path=input_path, 
        )
    
    indexer.index_datasets(reindex=reindex)

# ==================================================

def main():
# Check if the current working path is `notebook_search_docker``, if not terminate the program
    if os.path.basename(os.getcwd()) != 'notebook_search_docker': 
        print(f'Please navigate to `notebook_search_docker` directory and run: \n `python -m indexer.dataset_indexing`\n')
        return False
    
    data_dir = os.path.join(os.getcwd(), 'data/dataset')
    # Change `reindex` to True if you want to reindex the notebooks
    # index_datasets(data_dir=data_dir, source_name='Kaggle', query_source='PWC', preprocess_type='basic', reindex=True)
    # index_datasets(data_dir=data_dir, source_name='Zenodo', query_source='PWC', preprocess_type='basic', reindex=True)
    # index_datasets(data_dir=data_dir, source_name='Dryad', query_source='PWC', preprocess_type='basic', reindex=True)

# Go to 'notebook_search_docker/' dir and 
# run `python -m indexer.dataset_indexing` 
# Otherwise it won't work. 
if __name__ == '__main__': 
    main()
