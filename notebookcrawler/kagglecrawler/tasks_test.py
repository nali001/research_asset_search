# tasks.py 
# Ref: https://medium.com/@tonywangcn/how-to-build-docker-cluster-with-celery-and-rabbitmq-in-10-minutes-13fc74d21730 

from __future__ import absolute_import
from kagglecrawler import tasks
from pymongo import MongoClient


# Create client and collections
client = MongoClient('localhost', 27017) # change the ip and port to your mongo database's
db = client['kagglecrawler']
search_log_coll = db['search_log']
download_log_coll = db['download_log']
raw_notebook_coll = db['raw_notebooks']
task_log = db['task_log']

query = 'LSTM'
page_range = 10
try:
    num_modified = tasks.crawl_kaggle_notebooks(client=client, query=query, page_range=page_range, re_search=True)
    print(num_modified)
except Exception as exc:
    print(exc)


# @app.task(bind=True)
# def download_notebook(self, query, kernel_ref): 
#     try:
#         crawler.download_kernel_to_db(query=query, kernel_ref=kernel_ref, download_log_coll=download_log_coll, raw_notebook_coll=raw_notebook_coll)
#     except Exception as exc:
#         raise self.retry(exc=exc)
#     return True
