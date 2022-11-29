# distribution_notebook_crawling.py
# Incorporate multiprocessing to increase parallisation. 

import os 
import pandas as pd
from kagglecrawler.kaggle_api import AuthenticatedKaggleAPI

from pymongo import MongoClient

from multiprocessing import Pool


class KaggleNotebookCrawler: 
    ''' Crawl kaggle notebooks using new Kaggle API and store the raw notebooks into MongoDB.
    Here the MongoDB is used for concurrency, deduplication and progress control. 

    Schema: 
        - Raw notebooks: ['source_id', 'name', 'file_name', 'source', 'notebook_source_file']
        - search log: ['query', 'title', 'kernel_ref']
        - download log: ['query', 'title', 'kernel_ref']
    '''
    # METADATA_FILE_NAME = "kernel-metadata.json"

    def __init__(self):
        self.kaggle_api = AuthenticatedKaggleAPI()
        # self.KERNEL_DOWNLOAD_PATH = KERNEL_DOWNLOAD_PATH
        # self.KAGGLE_DOWNLOAD_LOG_FILE = KAGGLE_DOWNLOAD_LOG_FILE
        # self.KAGGLE_SEARCH_LOG_FILE = KAGGLE_SEARCH_LOG_FILE
        # self.df_queries = df_queries    

    def update_search_log(self, records, search_log_coll): 
        ''' Update search log 
        '''
        # check if the `records` is empty
        if not records: 
            return 0

        new_records = []
        for record in records: 
            key = {'kernel_ref': record['kernel_ref']}

            # check is the record already exists
            if not list(search_log_coll.find(key)): 
                new_records.append(record)

        # Check if the `new_records` is empty
        if new_records: 
            result = search_log_coll.insert_many(new_records)
            return len(new_records)
        else: 
            return 0
        
    def update_download_log(self, records, download_log_coll): 
        ''' Update download log
        '''
        # check if the `records` is empty
        if not records: 
            return 0

        new_records = []
        for record in records: 
            key = {'kernel_ref': record['kernel_ref']}

            # check is the record already exists
            if not list(download_log_coll.find(key)): 
                new_records.append(record)

        # Check if the `new_records` is empty
        if new_records: 
            result = download_log_coll.insert_many(new_records)
            return len(new_records)
        else: 
            return 0


    def update_notebooks(self, records, raw_notebook_coll): 
        ''' Update download log
        '''
        # check if the `records` is empty
        if not records: 
            return 0

        new_records = []
        for record in records: 
            key = {'source_id': record['source_id']}

            # check is the record already exists
            if not list(raw_notebook_coll.find(key)): 
                new_records.append(record)

        # Check if the `new_records` is empty
        if new_records: 
            result = raw_notebook_coll.insert_many(new_records)
            return len(new_records)
        else: 
            return 0
        

    def search_kernels_to_db(self, query, page_range, search_log_coll): 
        ''' Search Kaggle kernels using given query and store new records to MongoDB

        Returns: 
            - results: a list of dict in the form of {
                'query': query, 
                'title': kernel.title, 
                'kernel_ref': kernel.ref}
        '''
        records = self.kaggle_api.search_kernels(query, page_range)
        num_modified = self.update_search_log(records, search_log_coll)
        return records

    def download_kernel_to_db(self, query, kernel_ref, download_log_coll, raw_notebook_coll):
        ''' Download the kernels together with the metadata file to the disk

        Args: 
            - kernel_ref: the ID used by Kaggle to denote one notebook. 
            - search_log_coll: the destination MongoDB database for search logs
            - download_log_coll: the destination MongoDB database for download logs
            - notebook_coll: the destination MongoDB database for downloaded notebooks
        
        Return: 
            # - Boolean: Only True when the file is correctly downloaded or already exists. 

        For example, given kernel_ref = 'buddhiniw/breast-cancer-prediction', 
        there will be two files downloaded: 
            - buddhiniw_breast-cancer-prediction.ipynb
            - buddhiniw_breast-cancer-prediction.json
        '''

        # Check if the notebook already exists
        record = {'source_id': kernel_ref}
        if not list(raw_notebook_coll.find(record)): 
            # Download notebook from Kaggle 
            try: 
                print(f'[Pulling] {kernel_ref}')
                response = self.kaggle_api.download_kernel(kernel_ref)
            except Exception as e:
                # print(e) 
                print(f'[***FAIL] {kernel_ref}')
                return False
            metadata = response['metadata']
            blob = response['blob']
            raw_notebook = [{
                'source_id': metadata['ref'], 
                'name': metadata['title'], 
                'file_name': os.path.dirname(kernel_ref) + '_' + os.path.basename(kernel_ref), 
                'source': 'Kaggle', 
                'notebook_source_file': blob['source']
            }]

            download_log = [{
                'query': query, 
                'title': metadata['title'], 
                'kernel_ref': metadata['ref']
            }]
            # Insert new raw notebooks to database if no exists
            self.update_notebooks(raw_notebook, raw_notebook_coll)
            self.update_download_log(download_log, download_log_coll)
        else: 
            print(f'[!!EXIST] {kernel_ref}')
        return True


    def crawl_notebooks_to_db(self, ordered_query:tuple, page_range, search_log_coll, download_log_coll, raw_notebook_coll, re_search=False):
        ''' Search and download notebooks for each query 

        The notebooks will be downloaed to database. 

        Args: 
            - ordered_query: (index, query_text)
        '''
        print(f'---------------- Query [{ordered_query[0]+1}]: {ordered_query[1]} ----------------') 
        query = ordered_query[1]

        # If `re_search` is True, it will search the notebooks using `query` 
        if re_search==True: 
            records = self.search_kernels_to_db(query, page_range, search_log_coll)
            print(records)
        # If `re_search` is False, it will read from `search_log_coll` for a list of notebooks to be download 
        elif re_search==False: 
            key = {'query': query}
            try: 
                records = list(search_log_coll.find(key))
                if len(records): 
                    print(f'Found {len(records)} from search log.\n')
            except Exception as e:
                print(f'[SearchLog ERROR(self-defined)] There is no search log found!') 
        
        for record in records: 
            query = record['query'], 
            kernel_ref = record['kernel_ref']
            self.download_kernel_to_db(query, kernel_ref, download_log_coll, raw_notebook_coll)
        return True

    def export_raw_notebooks(self):
        pass


# --------------------------------- Usage examples
# def crawl_kaggle_notebooks(QUERY_FILE, page_range, re_search=False): 
#     # create database and collections
#     client = MongoClient('localhost', 27017) # change the ip and port to your mongo database's
#     db = client['kagglecrawler']
#     search_log_coll = db['search_log']
#     download_log_coll = db['download_log']
#     raw_notebook_coll = db['raw_notebooks']
#     task_log = db['task_log']
    
    
#     crawler = KaggleNotebookCrawler()

#     # Read queries
#     df_queries = pd.read_csv(QUERY_FILE)
#     # queries = ['wsi']
#     # df_queries = pd.DataFrame(queries, columns= ['queries'])
#     # print(df_queries)
#     def f(ordered_query):
#         result = crawler.crawl_notebooks_to_db(ordered_query, page_range, search_log_coll, download_log_coll, raw_notebook_coll, re_search)
#         return result

#     ordered_queries = list(enumerate(df_queries['query']))
#     with Pool(20) as p:
#         p.map(f, ordered_queries)
        
#     return True


# def main():
#     # Check if the current working path is `search_engine_app``, if not terminate the program
#     if os.path.basename(os.getcwd()) != 'notebookcrawler': 
#         print(f'Please navigate to `notebookcrawler` directory.')
#         return False
#     QUERY_FILE = os.path.join(os.getcwd(), 'Queries/test_queries.csv')
#     # crawl_kaggle_notebooks(QUERY_FILE, page_range=10, re_search=True)
    
#     # create database and collections
#     client = MongoClient('localhost', 27017) # change the ip and port to your mongo database's
#     db = client['kagglecrawler']
#     search_log_coll = db['search_log']
#     download_log_coll = db['download_log']
#     raw_notebook_coll = db['raw_notebooks']
#     task_log = db['task_log']
    
    
#     crawler = KaggleNotebookCrawler()

#     # Read queries
#     df_queries = pd.read_csv(QUERY_FILE)
#     # queries = ['wsi']
#     # df_queries = pd.DataFrame(queries, columns= ['queries'])
#     # print(df_queries)
#     def f(ordered_query):
#         # print(f'---------------- Query [{query[0]+1}]: {query[1]} ----------------') 
#         result = crawler.crawl_notebooks_to_db(ordered_query, page_range=10, search_log_coll=search_log_coll, download_log_coll=download_log_coll, raw_notebook_coll=raw_notebook_coll, re_search=True)
#         return result

#     ordered_queries = list(enumerate(df_queries['query']))
#     with Pool(20) as p:
#         p.map(f, ordered_queries)   

#     return True

if __name__ == '__main__':
    # Check if the current working path is `search_engine_app``, if not terminate the program
    if os.path.basename(os.getcwd()) != 'notebookcrawler': 
        print(f'Please navigate to `notebookcrawler` directory.')

    QUERY_FILE = os.path.join(os.getcwd(), 'Queries/pwc_queries.csv')
    # crawl_kaggle_notebooks(QUERY_FILE, page_range=10, re_search=True)
    
    # create database and collections
    client = MongoClient('localhost', 27017) # change the ip and port to your mongo database's
    db = client['kagglecrawler']
    search_log_coll = db['search_log']
    download_log_coll = db['download_log']
    raw_notebook_coll = db['raw_notebooks']
    task_log = db['task_log']
    
    
    crawler = KaggleNotebookCrawler()

    # Read queries
    df_queries = pd.read_csv(QUERY_FILE)
    # queries = ['wsi']
    # df_queries = pd.DataFrame(queries, columns= ['queries'])
    # print(df_queries)
    def f(ordered_query):
        # print(f'---------------- Query [{query[0]+1}]: {query[1]} ----------------') 
        result = crawler.crawl_notebooks_to_db(ordered_query, page_range=10, search_log_coll=search_log_coll, download_log_coll=download_log_coll, raw_notebook_coll=raw_notebook_coll, re_search=False)
        return result

    ordered_queries = list(enumerate(df_queries['query']))
    with Pool(50) as p:
        p.map(f, ordered_queries)

