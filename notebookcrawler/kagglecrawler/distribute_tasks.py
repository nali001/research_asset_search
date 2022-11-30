import os
import time
import numpy as np
import pandas as pd

from pymongo import MongoClient


class TaskSplitter: 
    def __init__(self, **kwargs): 
        for key, value in kwargs.items():
            setattr(self, key, value)

    def split_search_tasks(self, num_tasks, task_path):
        ''' Split search tasks and output each task to a .csv file
        '''

        # Read tasks from a central task file 
        central_task_log_coll = self.central_task_log_coll
        df_tasks = pd.DataFrame.from_dict(list(central_task_log_coll.find()))
        df_search_queries = df_tasks.loc[df_tasks['searched']==-1]

        # Split tasks into ten splits 
        search_tasks = np.array_split(df_search_queries, num_tasks)
        for i, task in enumerate(search_tasks):
            file_name = os.path.join(task_path, f'search_task_{i}.csv')
            # Save to csv files. 
            task.to_csv(file_name, index=False)
        return search_tasks


    def split_crawl_tasks(self, num_tasks, task_path): 
        ''' Split crawl tasks and output each task to a .csv file
        '''
        # Read tasks from a central task file 
        central_task_log_coll = self.central_task_log_coll
        df_tasks = pd.DataFrame.from_dict(list(central_task_log_coll.find()))

        if re_search==False: 
            df_download_queries = df_tasks.loc[(df_tasks['searched']>=0) & (df_tasks['downloaded']==-1)]
        else: 
            df_download_queries = df_tasks.loc[df_tasks['downloaded']==-1]

        # Split tasks into ten splits 
        crawl_tasks = np.array_split(df_download_queries, num_tasks)
        for i, task in enumerate(crawl_tasks):
            file_name = os.path.join(task_path, f'crawl_task_{i}.csv')
            # Save to csv files. 
            task.to_csv(file_name, index=False)
        return crawl_tasks


    def load_tasks(self, task_file):
        ''' Create new collection `task_log_coll`. It exists, delete it. 
        '''
        # Read tasks from csv file
        df_tasks = pd.read_csv(task_file)
        if '_id' in df_tasks.columns:
            df_tasks.drop(columns=['_id'], inplace=True)
        records = df_tasks.to_dict('records')

        # Create a new collection for local task log 
        task_log_coll = self.task_log_coll
        task_log_coll.delete_many({})

        task_log_coll.insert_many(records)
        return records
        


    def update_central_log(self): 
        ''' Update the central task log
        ''' 
        task_log_coll = self.task_log_coll
        central_task_log_coll = self.central_task_log_coll

        records = list(task_log_coll.find())
        # check if the `records` is empty
        if not records: 
            return 0
        
        for record in records: 
            record.pop('_id', None)
            key = {'query': record['query']}
            result = central_task_log_coll.replace_one(key, record, upsert=True)
        return len(records)



if __name__ == '__main__': 
    # Check if the current working path is `search_engine_app``, if not terminate the program
    if os.path.basename(os.getcwd()) != 'notebookcrawler': 
        print(f'Please navigate to `notebookcrawler` directory.')
    re_search = False
    client = MongoClient('localhost', 27017) # change the ip and port to your mongo database's
    db = client['kagglecrawler']
    # search_log_coll = db['search_log']
    # download_log_coll = db['download_log']
    # raw_notebook_coll = db['raw_notebooks']
    # notebook_metadata_coll = db['notebook_metadata_coll']
    task_log_coll = db['task_log']
    central_task_log_coll = db['central_task_log']

    # Create task_splitter
    kwargs = {
        'task_log_coll': task_log_coll, 
        'central_task_log_coll': central_task_log_coll, 
    }

    task_splitter = TaskSplitter(**kwargs)
    num_tasks = 10
    task_path = os.path.join(os.getcwd(), 'Tasks')

    # ------------------- Split search task ------------------ 
    # task_splitter.split_search_tasks(num_tasks, task_path)

    # ------------------- Split crawl task ------------------ 
    task_splitter.split_crawl_tasks(num_tasks, task_path)

    # ------------------- Load task ------------------- 
    # task_file = os.path.join(task_path, 'search_task_0.csv')
    # task_splitter.load_tasks(task_file)


