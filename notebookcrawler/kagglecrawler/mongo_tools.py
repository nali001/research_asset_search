import os
import time
import pandas as pd

from pymongo import MongoClient

client = MongoClient('localhost', 27017) # change the ip and port to your mongo database's
db = client['kagglecrawler']
search_log_coll = db['search_log']
download_log_coll = db['download_log']
raw_notebook_coll = db['raw_notebooks']
task_log = db['task_log']


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


def export_raw_notebooks():
    coll = raw_notebook_coll
    file_name = os.path.join(os.getcwd(), 'DB_exports/raw_notebook.csv')
    export_from_collection(coll, file_name)
    return True

def export_resources():
    export_search_log()
    export_download_log()
    export_raw_notebooks()
    return True

if __name__ == '__main__': 
    print(f'search_log_coll: {len(list(search_log_coll.find()))}')
    print(f'download_log_coll: {len(list(download_log_coll.find()))}')
    print(f'raw_notebook_coll: {len(list(raw_notebook_coll.find()))}')

    