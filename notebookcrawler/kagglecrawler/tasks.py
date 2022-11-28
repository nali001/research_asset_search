# tasks.py 
# Ref: https://medium.com/@tonywangcn/how-to-build-docker-cluster-with-celery-and-rabbitmq-in-10-minutes-13fc74d21730 

from __future__ import absolute_import
from kagglecrawler.celery import app
from pymongo import MongoClient
from kagglecrawler import distributed_notebook_crawling


# QUERY_FILE = os.path.join(os.getcwd(), 'notebooksearch/Queries/pwc_queries.csv')
# distributed_notebook_crawling.crawl_kaggle_notebooks(QUERY_FILE, page_range=10, re_search=True)

crawler = distributed_notebook_crawling.KaggleNotebookCrawler()

@app.task(bind=True) # set a retry delay, 10 equal to 10s
def crawl_kaggle_notebooks(self, client, query, page_range, re_search):
    db = client['kagglecrawler']
    search_log_coll = db['search_log']
    download_log_coll = db['download_log']
    raw_notebook_coll = db['raw_notebooks']
    task_log = db['task_log']
    print('Searching notebook begins')
    
    try:
        records = crawler.crawl_notebooks_to_db(query, page_range, search_log_coll, download_log_coll, raw_notebook_coll, re_search)
    except Exception as exc:
        raise self.retry(exc=exc)
    return records

# @app.task(bind=True)
# def download_notebook(self, query, kernel_ref): 
#     try:
#         crawler.download_kernel_to_db(query=query, kernel_ref=kernel_ref, download_log_coll=download_log_coll, raw_notebook_coll=raw_notebook_coll)
#     except Exception as exc:
#         raise self.retry(exc=exc)
#     return True
