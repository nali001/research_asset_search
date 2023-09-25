from elasticsearch_dsl import Index
import json
import os
import time

import pandas as pd
import datetime

from utils import utils
# from notebooksearch import notebook_retrieval
from elasticsearch import Elasticsearch

from .indexing_schema import NOTEBOOK_INDEX_SUMMARY

# ----------------------------------------------------------------------------------

class ElasticsearchIndexer():
    '''Index preprocessed notebooks with Elasticsearch. 

    Attrs: 
        - es: Elasticsearch client
        - index_name: Elasticsearch index name. 
        - notebook_path: The path for storing notebook files. 
        - source_name: 'Kaggle' or 'Github'. The repository source for notebooks
        - doc_type: 'preprocessed' or 'raw'. The document type for notebooks
    '''
    def __init__(self, es: Elasticsearch, source_name: str, doc_type:str, index_name:str, notebook_path:str): 
        self.es = es
        self.index_name = index_name
        self.notebook_path = notebook_path
        self.source_name = source_name
        self.doc_type = doc_type
        # self.source_file_name = source_file_name
    

    def index_notebooks(self, reindex = False): 
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
            # indexfiles = self.generate_index_files()
            if self.doc_type == 'preprocessed': 
                if self.source_name=='Github' or self.source_name=='Kaggle': 
                    root = self.notebook_path
                    count = 0
                    for path, _, files in os.walk(root):
                        for name in files:
                            indexfile= os.path.join(path, name)
                            index_content = utils.read_json_file(indexfile)
                            newRecord = {}
                            newRecord['id'] = index_content["html_url"]
                            for key in NOTEBOOK_INDEX_SUMMARY.keys():
                                newRecord[key] = index_content[key]
                    # for count, record in enumerate(indexfiles): 
                            try: 
                                res = es.index(index=index_name, id = newRecord["id"], body=newRecord)
                                print(f'Indexing {str(count+1)}-th record!\n')
                                count = count + 1
                            except Exception as e: 
                                print(e, "\n")
                                print(newRecord["name"])
                    es.indices.refresh(index=index_name)

            # elif self.doc_type == 'raw': 
            #     for count, record in enumerate(indexfiles): 
            #         try: 
            #             res = es.index(index=index_name, id = record["id"], body=record)
            #             print(f'Indexing {str(count+1)}-th raw notebook!\n')
            #         except Exception as e: 
            #             print(e, "\n")
            #             print(record["docid"])
            #         es.indices.refresh(index=index_name)
            else: 
                pass
        return True
# ----------------------------------------------------------------------------------

# ================= Below are the functions to generate different indexes =======================
# Depending on the content you want to include in the Elasticsearch index database. 

def index_preprocessed_notebooks(source_name=None, reindex=False):  
    ''' Index preprocessed notebooks, 
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

    # Index notebooks crawled from Github or Kaggle
    # github_notebook_path = os.path.join(os.getcwd(), 'notebooksearch', 'Github Notebooks')
    # indexer = ElasticsearchIndexer(es, "Github", "github_notebooks", github_notebook_path)
    notebook_path = f'./data/notebook/{source_name}/preprocessed_content/notebooks_summaries'
    print(notebook_path)
    current_date = str(datetime.date.today())
    indexer = ElasticsearchIndexer(
        es=es, 
        source_name=source_name, 
        doc_type="preprocessed", 
        index_name=f"{source_name.lower()}_notebooks_{current_date}", 
        notebook_path=notebook_path, 
        # source_file_name="Kaggle_updated_preprocessed_notebooks.csv"
        )
    
    indexer.index_notebooks(reindex=reindex)


def index_raw_notebooks(reindex=False):         
    ''' Index raw notebooks, 
    this will be used to download original notebooks from the index 
    '''
    # Try to reconnect to Elasticsearch for 10 times when failing
    # This is useful when Elasticsearch service is not fully online, 
    # which usually happens when starting all services at once. 
    for i in range(100): 
        es = utils.create_es_client()
        if es == None: 
            time.sleep(0.5)
            continue
        else: 
            break

    # Index notebooks crawled from Github or Kaggle
    # github_notebook_path = os.path.join(os.getcwd(), 'notebooksearch', 'Github Notebooks')
    # indexer = ElasticsearchIndexer(es, "Github", "github_notebooks", github_notebook_path)
    notebook_path = os.path.join(os.getcwd(), 'notebooksearch', 'Notebooks')
    indexer = ElasticsearchIndexer(
        es=es, 
        source_name="Kaggle", 
        doc_type="raw", 
        index_name="kaggle_raw_notebooks", 
        notebook_path=notebook_path, 
        # source_file_name="Kaggle_raw_notebooks.csv"
        )
    indexer.index_notebooks(reindex=reindex)



def index_github_summarization(reindex=False):         
    ''' Index summarization of the notebooks, 
    this addes summarizations to preprocessed notebooks
    and will be used from the retrieval 
    '''
    # Try to reconnect to Elasticsearch for 10 times when failing
    # This is useful when Elasticsearch service is not fully online, 
    # which usually happens when starting all services at once. 
    for i in range(100): 
        es = utils.create_es_client()
        if es == None: 
            time.sleep(0.5)
            continue
        else: 
            break

    notebook_path = os.path.join(os.getcwd(), '../data/notebook/')
    indexer = ElasticsearchIndexer(
        es=es, 
        source_name="Github", 
        doc_type="preprocessed", 
        index_name="kaggle_notebook_summarization", 
        notebook_path=notebook_path, 
        # source_file_name="Kaggle_summarization_fake_score.csv"
        )
    indexer.index_notebooks(reindex=reindex)


def index_kaggle_summarization(reindex=False):         
    ''' Index summarization of the notebooks, 
    this addes summarizations to preprocessed notebooks
    and will be used from the retrieval 
    '''
    # Try to reconnect to Elasticsearch for 10 times when failing
    # This is useful when Elasticsearch service is not fully online, 
    # which usually happens when starting all services at once. 
    for i in range(100): 
        es = utils.create_es_client()
        if es == None: 
            time.sleep(0.5)
            continue
        else: 
            break

    notebook_path = os.path.join(os.getcwd(), 'notebooksearch', 'Notebooks')
    indexer = ElasticsearchIndexer(
        es=es, 
        source_name="Kaggle", 
        doc_type="preprocessed", 
        index_name="kaggle_notebook_summarization", 
        notebook_path=notebook_path, 
        # source_file_name="Kaggle_summarization_fake_score.csv"
        )
    indexer.index_notebooks(reindex=reindex)

# ==================================================

def main():
# Check if the current working path is `search_engine_app``, if not terminate the program
    # if os.path.basename(os.getcwd()) != 'search_engine_app': 
    #     print(f'Please navigate to `search_engine_app` directory and run: \n `python -m notebooksearch.notebook_indexing`\n')
    #     return False

    # Change `reindex` to True if you want to reindex the notebooks
    # index_kaggle_summarization(reindex=True)
    # index_raw_notebooks(reindex=False)
    index_preprocessed_notebooks(source_name='Kaggle', reindex=True)

# Go to 'notebook_search_docker/' dir and 
# run `python -m indexer.notebook_indexing` 
# Otherwise it won't work. 
if __name__ == '__main__': 
    main()
