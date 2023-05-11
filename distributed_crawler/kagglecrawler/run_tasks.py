import os
import pandas as pd
from kagglecrawler import tasks
from pymongo import MongoClient
# from kagglecrawler import distributed_notebook_crawling



def crawl_kaggle_notebooks(query_file, page_range, re_search=False): 
    # Create client and collections
    client = MongoClient('mongo', 27017) # change the ip and port to your mongo database's

    # Read queries
    df_queries = pd.read_csv(query_file)
    # queries = ['wsi']
    # df_queries = pd.DataFrame(queries, columns= ['queries'])
    # print(df_queries)
    for i, query in enumerate(df_queries['query']): 
        print(f'---------------- Query [{i+1}]: {query} ----------------')
        result = tasks.crawl_kaggle_notebooks(client, query, page_range, re_search)
    return True

def main():
    # Check if the current working path is `search_engine_app``, if not terminate the program
    if os.path.basename(os.getcwd()) != 'notebookcrawler': 
        print(f'Please navigate to `notebookcrawler` directory.')
        return False
    QUERY_FILE = os.path.join(os.getcwd(), 'Queries/test_queries.csv')
    crawl_kaggle_notebooks(QUERY_FILE, page_range=10, re_search=True)
    return True
        
if __name__ == '__main__':
     main()
    