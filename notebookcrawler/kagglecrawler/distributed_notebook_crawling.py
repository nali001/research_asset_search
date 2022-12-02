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

from kagglecrawler import mongo_tools


class KaggleNotebookCrawler: 
    ''' Crawl kaggle notebooks using new Kaggle API and store the raw notebooks into MongoDB.
    Here the MongoDB is used for concurrency, deduplication and progress control. 

    Schema: 
        - raw notebooks: ['source_id', 'name', 'file_name', 'source', 'notebook_source_file']
        - search log: ['query', 'title', 'kernel_ref']
        - download log: ['query', 'title', 'kernel_ref']
        - task log: ['query', 'searched', 'downloaded']
    '''
    # METADATA_FILE_NAME = "kernel-metadata.json"

    def __init__(self, **kwargs):
        self.kaggle_api = AuthenticatedKaggleAPI()
        for key, value in kwargs.items():
            setattr(self, key, value)


    def add_tasks(self, records, task_log_coll): 
        ''' initialize task log 
        '''

        # check if the `records` is empty
        if not records: 
            return []

        new_records = []
        for record in records: 
            key = {'query': record['query']}
            # check is the record already exists
            if not list(task_log_coll.find(key)): 
                new_records.append(record)
        # Check if the `new_records` is empty
        if new_records: 
            result = task_log_coll.insert_many(new_records)
            return len(new_records)

    def update_task_log(self, records, task_log_coll): 
        ''' Update task log for changing `searched` and `downloaded` status
        '''

        # check if the `records` is empty
        if not records: 
            return 0
        
        for record in records: 
            key = {'query': record['query']}
            result = task_log_coll.replace_one(key, record, upsert=True)
        return len(records)


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
        ''' Update raw notebooks
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

    def update_notebook_metadata(self, records, notebook_metadata_coll): 
        ''' Update notebook metadata
        '''
        # check if the `records` is empty
        if not records: 
            return 0

        new_records = []
        for record in records: 
            key = {'ref': record['ref']}

            # check is the record already exists
            if not list(notebook_metadata_coll.find(key)): 
                new_records.append(record)

        # Check if the `new_records` is empty
        if new_records: 
            result = notebook_metadata_coll.insert_many(new_records)
            return len(new_records)
        else: 
            return 0
        

    def search_kernels_to_db(self, ordered_query, page_range, update=False): 
        ''' Search Kaggle kernels for one query and store new records to MongoDB

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
        search_log_coll = self.search_log_coll
        download_log_coll = self.download_log_coll
        records = []
        task_log = []
        key = {'query': query}
        num_search_records = len(list(search_log_coll.find(key)))
        # num_download_records = len(list(download_log_coll.find(key)))
        min_records = 1

        # Skip this turn and update task_log 
        if update==False and num_search_records>=min_records:
            print(f'[***SKIP] it already has {num_search_records} records in the search log. ')
            task_log = [{
                    'query': query, 
                    'searched': num_search_records, 
                    'downloaded': -1
                }]

        # Start to search notebooks
        else: 
            try: 
                records = self.kaggle_api.search_kernels(query, page_range)
                self.update_search_log(records, search_log_coll)
                task_log = [{
                    'query': query, 
                    'searched': len(records), 
                    'downloaded': -1
                }]
                
            except Exception as e:
                print(f'------------ Here is the error [[[SEARCH_KERNEL]]]')
                print(e)
                print(f'-------------\n\n') 
        
        if task_log:
            self.update_task_log(task_log, task_log_coll)
        return records

    def download_kernel_to_db(self, query:str, kernel_ref:str):
        ''' Download one Kaggle kernel. 

        Download the kernels together with the metadata file to the disk

        Args: 
            - query: str. the text of query
            - kernel_ref: the ID used by Kaggle to denote one notebook. 
            - download_log_coll: the destination MongoDB database for download logs
            - notebook_coll: the destination MongoDB database for downloaded notebooks
        
        Return: 
            # - Boolean: Only True when the file is correctly downloaded or already exists. 

        For example, given kernel_ref = 'buddhiniw/breast-cancer-prediction', 
        there will be two files downloaded: 
            - buddhiniw_breast-cancer-prediction.ipynb
            - buddhiniw_breast-cancer-prediction.json
        '''

        raw_notebook = []
        metadata = {}
        download_log = []
        raw_notebook_coll = self.raw_notebook_coll
        notebook_metadata_coll = self.notebook_metadata_coll
        download_log_coll = self.download_log_coll
        # Check if the notebook already exists
        # If yes, skip 
        record = {'source_id': kernel_ref}
        if list(raw_notebook_coll.find(record)) and list(notebook_metadata_coll.find(record)):
            print(f'[!!EXIST] {kernel_ref}')

        # If not, download notebook from Kaggle 
        else:       
            try: 
                print(f'[Pulling] {kernel_ref}')
                response = self.kaggle_api.download_kernel(kernel_ref)
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
            except Exception as e:
                print(f'[ERRORRRRRRRRR]\n{e}') 
                print(f'[***FAIL] {kernel_ref}')
                return False    
        
        # Insert new raw notebooks to database if no exists
        if raw_notebook: 
            self.update_notebooks(raw_notebook, raw_notebook_coll)
        
        if metadata: # print(metadata)
            self.update_notebook_metadata([metadata], notebook_metadata_coll)
        
        if download_log: 
            self.update_download_log(download_log, download_log_coll)
        return True


    def crawl_notebooks_to_db(self, ordered_query:tuple, page_range, re_search=False):
        ''' Search and download notebooks for each query 

        The notebooks will be downloaed to database. 

        Args: 
            - ordered_query: (index, query_text)
        '''
        task_log_coll = self.task_log_coll
        search_log_coll = self.search_log_coll
        download_log_coll = self.download_log_coll

        print(f'---------------- Crawl Query [{ordered_query[0]+1}]: {ordered_query[1]} ----------------') 
        task_log = []
        records = []
        query = ordered_query[1]
        min_records = 1
        key = {'query': query}
        
        # Check if the download log already has `min_records` records. 
        num_download_records = len(list(download_log_coll.find(key)))   
        if num_download_records>=min_records:
            print(f'[***SKIP] it already has {num_download_records} records in the download log. ')
            # Skip this turn and update task_log 
            num_search_records = len(list(search_log_coll.find(key)))
            task_log = [{
                    'query': query, 
                    'searched': num_search_records, 
                    'downloaded': num_download_records
                }]

        # If not, start to download notebooks
        else: 
            # If `re_search` is False, it will read from `search_log_coll` for kernel_ref
            if re_search==False: 
                key = {'query': query}
                try: 
                    records = list(search_log_coll.find(key))
                    if len(records): 
                        print(f'Found {len(records)} from search log.\n')
                except Exception as e:
                    print(f'[SearchLog ERROR(self-defined)] There is no search log found!') 
           
            # If `re_search` is True, it will search Kaggle for kernel_ref
            elif re_search==True: 
                records = self.search_kernels_to_db(ordered_query, page_range, update=False)


            for record in records: 
                query = record['query']
                kernel_ref = record['kernel_ref']
                self.download_kernel_to_db(query, kernel_ref)

            task_log = [{
                'query': query, 
                'searched': len(records), 
                'downloaded': len(records)
                }]
        if task_log: 
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
    notebook_metadata_coll = db['notebook_metadata']
    task_log_coll = db['task_log']
    

    # Controlling parameters
    re_search = False
    task_number = 0       
    span = 100
    task_name = 'crawl'


    # Create crawler
    kwargs = {
        'search_log_coll': search_log_coll, 
        'download_log_coll': download_log_coll, 
        'task_log_coll': task_log_coll, 
        'raw_notebook_coll': raw_notebook_coll, 
        'notebook_metadata_coll': notebook_metadata_coll
    }
    crawler = KaggleNotebookCrawler(**kwargs)
    
    # Initialize task_log if empty
    if not list(task_log_coll.find()): 
        QUERY_FILE = os.path.join(os.getcwd(), 'Queries/pwc_queries.csv')
        df_pwc_queries = pd.read_csv(QUERY_FILE)
        df_tasks = pd.DataFrame(df_pwc_queries['query'])
        df_tasks['searched'] = 0
        df_tasks['downloaded'] = 0
        records = df_tasks.to_dict('records')
        crawler.add_tasks(records, task_log_coll)
    

    def multiprocess_search(ordered_query):
        # Sleep for random seconds to avoid request flooding.  
        time.sleep(np.random.randint(1, 7))
        result = crawler.search_kernels_to_db(ordered_query, page_range=10, update=False)
        return result

    def multiprocess_crawl(ordered_query):
        # Sleep for random seconds to avoid request flooding.  
        time.sleep(np.random.randint(1, 10))
        result = crawler.crawl_notebooks_to_db(ordered_query, page_range=10, re_search=re_search)
        return result

    
    start_time = time.time()
    # Run 15 rounds, 
    # for each round, only use the first `span` size of queries
    for i in range(15): 
        # Read the most updated tasks
        df_tasks = pd.DataFrame.from_dict(list(task_log_coll.find()))
        df_search_queries = df_tasks.loc[df_tasks['searched']==-1]

        if re_search==False: 
            df_download_queries = df_tasks.loc[(df_tasks['searched']>=0) & (df_tasks['downloaded']==-1)]
        else: 
            df_download_queries = df_tasks.loc[df_tasks['downloaded']==-1]
        
        print(f'===== Round [{i}] =====')
        # --------------------- For searching ----------------------
        if task_name=='search': 
            if df_search_queries.empty: 
                print(f'Congratulations! search_task_{task_number} is finished.')
                break
            candidate_queries = df_search_queries.iloc[0:span]
            ordered_queries = list(enumerate(candidate_queries['query']))
            # Create multiple processes
            num_processes = 10
            print(f'Number of processes: {num_processes}')
            with Pool(num_processes) as p:
                p.map(multiprocess_search, ordered_queries)
                elapsed=int(time.time()-start_time)
                print(f'[Summary] {(i+1)*span} queries processed!\nElapsed time: {str(timedelta(seconds=elapsed))}\n\n')
                remote_path = f'notebook_search_docker/notebookcrawler/DB_exports/search_task_{task_number}/'
                mongo_tools.auto_save(remote_path)
        # ---------------------------------------------------------
        
        # --------------------- For crawling ----------------------
        elif task_name=='crawl': 
            if df_download_queries.empty: 
                print(f'Congratulations! crawl_task_{task_number} is finished.')
                break
            candidate_queries = df_download_queries.iloc[0:span]
            ordered_queries = list(enumerate(candidate_queries['query']))
            # Create multiple processes
            num_processes = 5
            with Pool(num_processes) as p:
                p.map(multiprocess_crawl, ordered_queries)
                elapsed=int(time.time()-start_time)
                print(f'[Summary] {(i+1)*span} queries processed!\nElapsed time: {str(timedelta(seconds=elapsed))}\n\n')
                remote_path = f'notebook_search_docker/notebookcrawler/DB_exports/crawl_task_{task_number}/'
                mongo_tools.auto_save(remote_path)
        # ---------------------------------------------------------

