# distribution_notebook_crawling.py
# Incorporate multiprocessing to increase parallisation. 

import os 
import time
from datetime import timedelta

import numpy as np
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

    def update_task_log(self, records, task_log_coll): 
        ''' Update task log 
        '''
        # check if the `records` is empty
        if not records: 
            return 0
        key = {'query': record['query']}
        for record in records: 
            for i in ['searched', 'downloaded']: 
                if record[i]: 
                    result = task_log_coll.update_one(key, {'$inc': {i: record[i]}}, upsert=True)
        return records

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
        

    def search_kernels_to_db(self, ordered_query, page_range, task_log_coll, search_log_coll, update=False): 
        ''' Search Kaggle kernels using given query and store new records to MongoDB

        Args: 
            - update: Boolean. If True, the search log will be updated using new searching results.  
                otherwise, if the number of notebooks w.r.t each query is >15, then the query is not used for searching. 

        Returns: 
            - results: a list of dict in the form of {
                'query': query, 
                'title': kernel.title, 
                'kernel_ref': kernel.ref}
        '''
        print(f'---------------- Search Query [{ordered_query[0]+1}]: {ordered_query[1]} ----------------') 
        query = ordered_query[1]

        # Check if the query has been searched
        records = []
        key = {'query': query}
        num_records = 15
        if update==False and len(list(search_log_coll.find(key)))>num_records:
            print(f'[***SKIP] it already has more than {num_records} records in the search log. ')
            return records
        try: 
            records = self.kaggle_api.search_kernels(query, page_range)
            self.update_search_log(records, search_log_coll)

            task_log = [{
                'query': query, 
                'searched': 1, 
                'downloaded': 0
            }]
            self.update_task_log(task_log, task_log_coll)
        except Exception as e:
            print(f'------------ Here is the error [[[SEARCH_KERNEL]]]')
            print(e)
            print(f'-------------\n\n') 
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
        # print(f'---------------- Query: {query} ----------------') 
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


    def crawl_notebooks_to_db(self, ordered_query:tuple, page_range, task_log_coll, search_log_coll, download_log_coll, raw_notebook_coll, re_search=False):
        ''' Search and download notebooks for each query 

        The notebooks will be downloaed to database. 

        Args: 
            - ordered_query: (index, query_text)
        '''
        print(f'---------------- Crawl Query [{ordered_query[0]+1}]: {ordered_query[1]} ----------------') 
        query = ordered_query[1]
        # If `re_search` is True, it will search the notebooks using `query` 
        if re_search==True: 
            records = self.search_kernels_to_db(ordered_query, page_range, search_log_coll, update=True)
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

        task_log = [{
                'query': query, 
                'searched': 1, 
                'downloaded': 1
            }]
        self.update_task_log(task_log, task_log_coll)

        return True


if __name__ == '__main__':
    # Check if the current working path is `search_engine_app``, if not terminate the program
    if os.path.basename(os.getcwd()) != 'notebookcrawler': 
        print(f'Please navigate to `notebookcrawler` directory.')

    # create database and collections
    client = MongoClient('localhost', 27017) # change the ip and port to your mongo database's
    db = client['kagglecrawler']
    search_log_coll = db['search_log']
    download_log_coll = db['download_log']
    raw_notebook_coll = db['raw_notebooks']
    task_log = db['task_log']

    QUERY_LOG_FILE = os.path.join(os.getcwd(), 'Queries/pwc_log_queries.csv')
    re_search = False
    
    # Create crawler
    crawler = KaggleNotebookCrawler()

    def multiprocess_crawl(ordered_query):
        # Sleep for random seconds to avoid request flooding.  
        # time.sleep(np.random.randint(1, 7))
        result = crawler.crawl_notebooks_to_db(ordered_query, page_range=10, task_log=task_log, search_log_coll=search_log_coll, download_log_coll=download_log_coll, raw_notebook_coll=raw_notebook_coll, re_search=re_search)
        return result

    def multiprocess_search(ordered_query):
        # Sleep for random seconds to avoid request flooding.  
        time.sleep(np.random.randint(1, 7))
        result = crawler.search_kernels_to_db(ordered_query, page_range=10, task_log=task_log, search_log_coll=search_log_coll, update=False)
        return result

    
    start_time = time.time()
    for i in range(10): 
        if re_search==True: 
            # Read query log from disk
            df_queries_log = pd.read_csv(QUERY_LOG_FILE)
            # Filter out queries that have not been crawled
            df_queries = df_queries_log.loc[df_queries_log['crawled']==0]
            
        else: 
            # Read query log from search log
            df_queries = pd.DataFrame.from_dict(list(search_log_coll.find()))

        # Split all the queries into small sets of `span` size
        span = 100
        craw_queries = df_queries.iloc[0:span]
        ordered_queries = list(enumerate(craw_queries['query']))
        
        # Create multiple processes
        num_processes = 1
        with Pool(num_processes) as p:
            p.map(multiprocess_crawl, ordered_queries)
            elapsed=int(time.time()-start_time)
            print(f'Elapsed time: {str(timedelta(seconds=elapsed))}\n')
            print(f'Updated notebooks for {span} queries!\n')

            # Update query log 
            if re_search==True: 
                df_queries_log.loc[craw_queries.index, 'crawled'] = 1
                df_queries_log.to_csv(QUERY_LOG_FILE, index=False)



