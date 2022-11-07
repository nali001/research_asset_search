from elasticsearch_dsl import Index
import json
import os
import time

import pandas as pd

from notebooksearch import utils
from elasticsearch import Elasticsearch

def open_file(file):
    read_path = file
    with open(read_path, "r", errors='ignore') as read_file:
        data = json.load(read_file)
    return data

# ----------------------------------------------------------------------------------

class ElasticsearchIndexer():
    ''' Build an Elasticsearch index. 
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

    def index_notebooks(self, reindex = False): 
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
            indexfiles = self.generate_index_files()
            if self.source_name == 'Github': 
                for count, record in enumerate(indexfiles): 
                    try: 
                        res = es.index(index=index_name, id = record["git_url"], body=record)
                        print(f'Indexing {str(count+1)}-th recode!\n')
                    except Exception as e: 
                        print(e, "\n")
                        print(record["name"])
                    es.indices.refresh(index=index_name)
            elif self.source_name == 'Kaggle': 
                for count, record in enumerate(indexfiles): 
                    try: 
                        res = es.index(index=index_name, id = record["kaggle_id"], body=record)
                        print(f'Indexing {str(count+1)}-th recode!\n')
                    except Exception as e: 
                        print(e, "\n")
                        print(record["name"])
                    es.indices.refresh(index=index_name)
        return True
# ----------------------------------------------------------------------------------

def index_kaggle_notebooks(reindex=False):         
    # Try to reconnect to Elasticsearch for 10 times when failing
    # This 
    for i in range(100): 
        es = utils.create_es_client()
        if es == None: 
            time.sleep(0.5)
            continue
        else: 
            break

    # Index notebooks crawled from Github
    # github_notebook_path = os.path.join(os.getcwd(), 'notebooksearch', 'Github Notebooks')
    # indexer = ElasticsearchIndexer(es, "Github", "github_notebooks", github_notebook_path)
    kaggle_notebook_path = os.path.join(os.getcwd(), 'notebooksearch', 'Notebooks', 'Kaggle')
    indexer = ElasticsearchIndexer(es, "Kaggle", "kaggle_notebooks", kaggle_notebook_path)
    indexer.index_notebooks(reindex=reindex)

def main():
# Check if the current working path is `search_engine_app``, if not terminate the program
    if os.path.basename(os.getcwd()) != 'search_engine_app': 
        print(f'Please navigate to `search_engine_app` directory and run: \n `python -m notebooksearch.notebook_crawling`\n')
        return False
    # Change `reindex` to Tur if you want to reindex the notebooks
    index_kaggle_notebooks(reindex=True)

# If using `python -m notebooksearch.notebook_indexing`, 
# `__name__` will be `__main__`
if __name__ == '__main__': 
    main()
