from elasticsearch_dsl import Index
import json
import os
import time

import pandas as pd

from utils import utils
# from notebooksearch import notebook_retrieval
from elasticsearch import Elasticsearch


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
    def __init__(self, es: Elasticsearch, source_name: str, doc_type:str, index_name:str, notebook_path:str, source_file_name:str): 
        self.es = es
        self.index_name = index_name
        self.notebook_path = notebook_path
        self.source_name = source_name
        self.doc_type = doc_type
        self.source_file_name = source_file_name
    
    def generate_index_files(self) -> list:
        ''' Generate a list of index files to be indexed by Elasticsearch. 

        Each index file is in the form of dictionary. 
        Depending on the source name, the index uses different schema. 
        '''
        indexfiles =[]
        # Index preprocessed notebooks
        if self.doc_type == 'preprocessed': 
            if self.source_name == 'Github': 
                root = self.notebook_path
                for path, _, files in os.walk(root):
                    for name in files:
                        indexfile= os.path.join(path, name)
                        indexfile = utils.read_json_file(indexfile)
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
                # ['source_id', 'name', 'file_name', 'html_url', 'description', 'source', 'docid', 'language', 
                # 'num_cells', 'num_code_cells', 'num_md_cells', 'len_md_text']
                df_notebooks = pd.read_csv(os.path.join(self.notebook_path, self.source_file_name))
                indexfiles =  df_notebooks.to_dict('records')
            else: 
                print("Notebook source is unknown, please specify a scheme.")

        # Index raw notebooks
        # ['docid', 'source_id', 'name', 'file_name', 'source', 'notebook_source_file']
        elif self.doc_type == 'raw': 
            root = self.notebook_path
            df_notebooks = pd.read_csv(os.path.join(self.notebook_path, self.source_file_name))
            indexfiles =  df_notebooks.to_dict('records')
        else: 
            print("Notebook type is unknown, please specify a doc_type.")
        return indexfiles

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
            indexfiles = self.generate_index_files()
            if self.doc_type == 'preprocessed': 
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
                            res = es.index(index=index_name, id = record["docid"], body=record)
                            print(f'Indexing {str(count+1)}-th recode!\n')
                        except Exception as e: 
                            print(e, "\n")
                            print(record["name"])
                        es.indices.refresh(index=index_name)
            elif self.doc_type == 'raw': 
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

def index_kaggle_notebooks(reindex=False):  
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
    notebook_path = os.path.join(os.getcwd(), 'notebooksearch', 'Notebooks')
    indexer = ElasticsearchIndexer(
        es=es, 
        source_name="Kaggle", 
        doc_type="preprocessed", 
        index_name="kaggle_notebooks", 
        notebook_path=notebook_path, 
        source_file_name="Kaggle_updated_preprocessed_notebooks.csv")
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
        source_file_name="Kaggle_raw_notebooks.csv")
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
        source_file_name="Kaggle_summarization_fake_score.csv")
    indexer.index_notebooks(reindex=reindex)

    # # Test the new index using notebook retrieval
    # query = "test"
    # query_params={
    #     "page": "1",
    #     "query": query,
    #     "filter": "",
    #     "facet": "",
    # }
    # index_name = "kaggle_notebook_summarization"
    # searcher = notebook_retrieval.NotebookRetriever(query_params, index_name)
    # search_results = searcher.retrieve_notebooks()
    # print(f'============ Retrieval test for index [{index_name}] ==========')
    # print(f"{search_results['results'][0]['summarization_t5']}\n")

def main():
# Check if the current working path is `search_engine_app``, if not terminate the program
    # if os.path.basename(os.getcwd()) != 'search_engine_app': 
    #     print(f'Please navigate to `search_engine_app` directory and run: \n `python -m notebooksearch.notebook_indexing`\n')
    #     return False

    # Change `reindex` to True if you want to reindex the notebooks
    # index_kaggle_summarization(reindex=True)
    index_raw_notebooks(reindex=False)

# Go to 'notebook_search_docker/' dir and 
# run `python -m indexer.notebook_indexing` 
# Otherwise it won't work. 
if __name__ == '__main__': 
    main()
