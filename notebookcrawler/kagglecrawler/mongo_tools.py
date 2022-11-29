from pymongo import MongoClient
client = MongoClient('localhost', 27017) # change the ip and port to your mongo database's
db = client['kagglecrawler']
search_log_coll = db['search_log']
download_log_coll = db['download_log']
raw_notebook_coll = db['raw_notebooks']
task_log = db['task_log']

if __name__ == '__main__': 
    print(f'search_log_coll: {len(list(search_log_coll.find()))}')
    print(f'download_log_coll: {len(list(download_log_coll.find()))}')
    print(f'raw_notebook_coll: {len(list(raw_notebook_coll.find()))}')
        # print(doc)