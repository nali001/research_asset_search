import os
import time
import pandas as pd

from pymongo import MongoClient

import subprocess

client = MongoClient('localhost', 27017) # change the ip and port to your mongo database's
db = client['kagglecrawler']
search_log_coll = db['search_log']
download_log_coll = db['download_log']
raw_notebook_coll = db['raw_notebooks']
notebook_metadata_coll = db['notebook_metadata']
central_task_log_coll = db['central_task_log']
task_log_coll = db['task_log']


def export_from_collection(coll, file_name, timestamp): 
    ''' Export collection to one .csv file'''
    coll_files = list(coll.find())
    df_coll_file = pd.DataFrame.from_dict(coll_files)

    # Add time stamp to exported file
    name = os.path.basename(file_name)
    export_dir = os.path.join(os.path.dirname(file_name), f'exports_{timestamp}')
    if not os.path.exists(export_dir):
        os.mkdir(export_dir)
    stamped_file_name = os.path.join(export_dir, name)
    df_coll_file.to_csv(stamped_file_name, index=False)
    print(f'Exported [{coll.name}] collection to {stamped_file_name}')
    return True

def export_search_log(timestamp): 
    coll = search_log_coll
    file_name = os.path.join(os.getcwd(), 'DB_exports/search_log.csv')
    export_from_collection(coll, file_name, timestamp)
    return True
    

def export_download_log(timestamp): 
    coll = download_log_coll
    file_name = os.path.join(os.getcwd(), 'DB_exports/download_log.csv')
    export_from_collection(coll, file_name, timestamp)
    return True

def export_task_log(timestamp): 
    coll = task_log_coll
    file_name = os.path.join(os.getcwd(), 'DB_exports/task_log.csv')
    export_from_collection(coll, file_name, timestamp)
    return True 

def export_central_task_log(timestamp): 
    coll = central_task_log_coll
    file_name = os.path.join(os.getcwd(), 'DB_exports/central_task_log.csv')
    export_from_collection(coll, file_name, timestamp)
    return True 

def export_raw_notebooks(timestamp):
    coll = raw_notebook_coll
    file_name = os.path.join(os.getcwd(), 'DB_exports/raw_notebook.csv')
    export_from_collection(coll, file_name, timestamp)
    return True


def export_notebook_metadata(timestamp):
    coll = notebook_metadata_coll
    file_name = os.path.join(os.getcwd(), 'DB_exports/notebook_metadata.csv')
    export_from_collection(coll, file_name, timestamp)
    return True

def export_resources():
    timestamp = int(time.time())
    export_search_log(timestamp)
    export_download_log(timestamp)
    export_raw_notebooks(timestamp)
    export_task_log(timestamp)
    export_central_task_log(timestamp)
    export_notebook_metadata(timestamp)
    return True

def get_coll_status(): 
    print(f'-------------- Collection status ---------------')
    print(f'central_task_log_coll: {len(list(central_task_log_coll.find()))}')
    print(f'task_log_coll: {len(list(task_log_coll.find()))}')
    print(f'search_log_coll: {len(list(search_log_coll.find()))}')
    print(f'download_log_coll: {len(list(download_log_coll.find()))}')
    print(f'raw_notebook_coll: {len(list(raw_notebook_coll.find()))}')
    print(f'notebook_metadata_coll: {len(list(notebook_metadata_coll.find()))}')
    print(f'-----------------------------------------------')


def get_task_status(): 
    df_tasks = pd.DataFrame.from_dict(list(task_log_coll.find()))
    searched = df_tasks.loc[df_tasks.searched>=0]
    downloaded = df_tasks.loc[df_tasks.downloaded>=0]
    un_searched = df_tasks.loc[df_tasks.searched==-1]
    un_downloaded = df_tasks.loc[df_tasks.downloaded==-1]
    zero_searched = df_tasks.loc[df_tasks.searched==0]
    zero_downloaded = df_tasks.loc[df_tasks.downloaded==0]
    
    print(f'\n----------------- Task status -----------------')
    print(f'>>> Query <<<')
    print(f'searched: {len(searched)}')
    print(f'un_searched: {len(un_searched)}')
    print(f'zero_searched: {len(zero_searched)}')
    print(f'downloaded: {len(downloaded)}')
    print(f'un_downloaded: {len(un_downloaded)}')
    print(f'zero_downloaded: {len(zero_downloaded)}')

    print(f'\n>>> Notebook <<<')
    print(f'seached notebooks: {len(list(search_log_coll.find()))}')
    print(f'download notebooks: {len(list(raw_notebook_coll.find()))}')
    print(f'download metadata: {len(list(notebook_metadata_coll.find()))}')
    print(f'------------------------------------------------')

def real_time_status(): 
    for i in range(1000): 
        get_task_status()
        time.sleep(10)

def auto_save(remote_path): 
    # Export resources to Db_exports
    export_resources()
    sh_file = os.path.join(os.getcwd(), 'upload_task_data.sh')
    rc = subprocess.call(f'{sh_file} {remote_path}', shell=True)
    print(f'Autosave to na_surf:{remote_path}:)')



if __name__ == '__main__': 
    real_time_status()
    # get_coll_status()
    # export_resources()
    # auto_save()

    