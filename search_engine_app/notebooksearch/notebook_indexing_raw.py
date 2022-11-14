# notebook_indexing_raw.py
''' Mainly for indecing raw notebooks into Elasticsearch database
'''

from elasticsearch_dsl import Index

import os
import time

import pandas as pd

from notebooksearch import utils
from elasticsearch import Elasticsearch


# ----------------------------------------------------------------------------------

class ElasticsearchRawIndexer():
    ''' Index raw notebooks using Elasticsearch. 
    '''
    def __init__(self, es: Elasticsearch, source_name: str, index_name: str, notebook_path: str): 
        self.es = es
        self.index_name = index_name
        self.notebook_path = notebook_path
        self.source_name = source_name
    
    def generate_index_files(self) -> list:
        ''' Generate a list of index files to be indexed by Elasticsearch. 

        Each index file is in the form of dictionary. 
        Depending on the source name, the index uses different schema. 
        '''
        indexfiles =[]
        if self.source_name == 'Github': 
            root = self.notebook_path
            for path, _, files in os.walk(root):
                for name in files:
                    indexfile= os.path.join(path, name)
                    indexfile = open_file(indexfile)
                    newRecord={
                        "name":indexfile["name"],
                        "full_name":indexfile["full_name"],
                        "stargazers_count":indexfile["stargazers_count"],
                        "forks_count":indexfile["forks_count"],
                        "description":indexfile["description"],
                        "size":indexfile["size"],
                        "language": indexfile["language"],
                        "html_url":indexfile["html_url"],
                        "git_url":indexfile["git_url"], 
                        "id":indexfile["git_url"], 
                        "source": "Github", 
                    }
                    indexfiles.append(newRecord)

        elif self.source_name == 'Kaggle': 
            root = self.notebook_path
            df_notebooks = pd.read_csv(os.path.join(root, "es_kaggle_notebooks.csv"))
            indexfiles =  df_notebooks.to_dict('records')
        else: 
            print("Notebook source is unknown, please specify a scheme.")
        return indexfiles

    def index_raw_notebooks(self, reindex = False): 
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
            root = self.notebook_path
            df_notebooks = pd.read_csv(os.path.join(root, "es_raw_notebooks.csv"))
            indexfiles =  df_notebooks.to_dict('records')
            for count, record in enumerate(indexfiles): 
                try: 
                    res = es.index(index=index_name, id = record["docid"], body=record)
                    print(f'Indexing {str(count+1)}-th raw notebook!\n')
                except Exception as e: 
                    print(e, "\n")
                    print(record["docid"])
                es.indices.refresh(index=index_name)
        return True
# ----------------------------------------------------------------------------------

def index_raw_notebooks(reindex=False):         
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
    raw_notebook_path = os.path.join(os.getcwd(), 'notebooksearch', 'Raw_notebooks')
    indexer = ElasticsearchRawIndexer(es, "Multiple sources", "raw_notebooks", raw_notebook_path)
    indexer.index_notebooks(reindex=reindex)

def main():
# Check if the current working path is `search_engine_app``, if not terminate the program
    if os.path.basename(os.getcwd()) != 'search_engine_app': 
        print(f'Please navigate to `search_engine_app` directory and run: \n `python -m notebooksearch.notebook_crawling`\n')
        return False
    # Change `reindex` to Tur if you want to reindex the notebooks
    index_raw_notebooks(reindex=True)

# If using `python -m notebooksearch.notebook_indexing`, 
# `__name__` will be `__main__`
if __name__ == '__main__': 
    main()
