import os
import time
import pandas as pd

from pymongo import MongoClient

client = MongoClient('localhost', 27017) # change the ip and port to your mongo database's
db = client['kagglecrawler']
search_log_coll = db['search_log']
download_log_coll = db['download_log']
raw_notebook_coll = db['raw_notebooks']
notebook_metadata_coll = db['notebook_metadata_coll']
central_task_log_coll = db['central_task_log_coll']
task_log_coll = db['task_log']


def export_from_collection(coll, file_name): 
    ''' Export collection to one .csv file'''
    coll_files = list(coll.find())
    df_coll_file = pd.DataFrame.from_dict(coll_files)

    # Add time stamp to exported file
    timestamp = int(time.time())
    names = os.path.basename(file_name).split('.')
    stamped_name = names[0]+'_'+str(timestamp)+'.'+names[1]
    stamped_file_name = os.path.join(os.path.dirname(file_name), stamped_name)
    df_coll_file.to_csv(stamped_file_name, index=False)
    print(f'Exported {coll} collection to {stamped_file_name}')
    return True

def export_search_log(): 
    coll = search_log_coll
    file_name = os.path.join(os.getcwd(), 'DB_exports/search_log.csv')
    export_from_collection(coll, file_name)
    return True
    

def export_download_log(): 
    coll = download_log_coll
    file_name = os.path.join(os.getcwd(), 'DB_exports/download_log.csv')
    export_from_collection(coll, file_name)
    return True

def export_task_log(): 
    coll = task_log_coll
    file_name = os.path.join(os.getcwd(), 'DB_exports/task_log.csv')
    export_from_collection(coll, file_name)
    return True 


def export_raw_notebooks():
    coll = raw_notebook_coll
    file_name = os.path.join(os.getcwd(), 'DB_exports/raw_notebook.csv')
    export_from_collection(coll, file_name)
    return True


def export_notebook_metadata():
    coll = notebook_metadata_coll
    file_name = os.path.join(os.getcwd(), 'DB_exports/notebook_metadata.csv')
    export_from_collection(coll, file_name)
    return True

def export_resources():
    export_search_log()
    export_download_log()
    export_raw_notebooks()
    export_task_log()
    export_notebook_metadata()
    return True

def get_coll_status(): 
    print(f'-------------- Collection status ---------------')
    print(f'search_log_coll: {len(list(search_log_coll.find()))}')
    print(f'download_log_coll: {len(list(download_log_coll.find()))}')
    print(f'raw_notebook_coll: {len(list(raw_notebook_coll.find()))}')
    print(f'task_log_coll: {len(list(task_log_coll.find()))}')
    print(f'notebook_metadata_coll: {len(list(notebook_metadata_coll.find()))}')
    print(f'\n-----------------------------------------------')


def get_task_status(): 
    df_tasks = pd.DataFrame.from_dict(list(task_log_coll.find()))
    un_searched = df_tasks.loc[df_tasks.searched==-1]
    un_downloaded = df_tasks.loc[df_tasks.downloaded==-1]
    zero_searched = df_tasks.loc[df_tasks.searched==0]
    zero_downloaded = df_tasks.loc[df_tasks.downloaded==0]
    
    print(f'\n----------------- Task status -----------------')
    print(f'seached notebooks: {len(list(search_log_coll.find()))}')
    print(f'download notebooks: {len(list(download_log_coll.find()))}')
    print(f'un_searched query: {len(un_searched)}')
    print(f'un_downloaded query: {len(un_downloaded)}')
    print(f'zero_searched query: {len(zero_searched)}')
    print(f'zero_downloaded query: {len(zero_downloaded)}')
    print(f'------------------------------------------------')

def real_time_status(): 
    for i in range(1000): 
        get_task_status()
        time.sleep(10)



if __name__ == '__main__': 
    real_time_status()
    # export_resources()

    