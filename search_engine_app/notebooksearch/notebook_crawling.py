import os 
import time
import pandas as pd
import kaggle
import json

class NotebookCrawler: 
    pass


class KaggleNotebookCrawler: 
    METADATA_FILE_NAME = "kernel-metadata.json"

    def __init__(self, df_queries, KERNEL_DOWNLOAD_PATH, KAGGLE_NOTEBOOK_LOG_FILE):
        self.KERNEL_DOWNLOAD_PATH = KERNEL_DOWNLOAD_PATH
        self.KAGGLE_NOTEBOOK_LOG_FILE = KAGGLE_NOTEBOOK_LOG_FILE
        self.df_queries = df_queries    

    def search_kernels(self, query): 
        ''' Search Kaggle kernels using given query
        '''
        print(f'------------- Query: {query} -------------')
        kernels = []
        for page in range(1, 100): 
            kernel_list = []
            try: 
                kernel_list = kaggle.api.kernels_list(search=query, page=page)
                print(f'Crawling page {page}')                
                if len(kernel_list) == 0: 
                    break
                else: 
                    kernels.extend(kernel_list)
            # Skip the pages that cause ApiException
            except kaggle.rest.ApiException as e:  
                # print(e)
                continue

        # Extract the `title` and the `ref` of returned Kaggle kernels
        results = []
        for kernel in kernels:
            results.append({
                'query': query, 
                'title': kernel.title, 
                'ref': kernel.ref})
        
        print('\n')
        return results

    def download_kernels(self, query, kernel_ref): 
        download_path = self.KERNEL_DOWNLOAD_PATH + "/"

        # Check if the file already downloaded
        if self.file_exists(query, kernel_ref): 
            return 
        
        try: 
            kaggle.api.kernels_pull(kernel_ref, download_path, metadata=True)
        except Exception as err: 
            print("Exception: ", err)
            return
        
        # Rename the metadata file
        try: 
            os.rename(download_path + self.METADATA_FILE_NAME, download_path + os.path.basename(kernel_ref + ".json"))
        except FileNotFoundError:
            pass

    def file_exists(self, query, kernel_ref): 
        file_path = self.KERNEL_DOWNLOAD_PATH + "/" + os.path.basename(kernel_ref) + ".ipynb" 
        if os.path.exists(file_path): 
            return True
        else: 
            return False
        
    def has_results(kernel_list): 
        if len(kernel_list) == 0:
            return False
        else: 
            return True   

    def crawl_notebooks(self):
        ''' Search and download notebooks using given queries 
        '''
        df_queries = self.df_queries
        notebooks = []

        # Search notebooks for each query
        for query in df_queries['queries']: 
            notebooks.extend(self.search_kernels(query))
        df_notebooks = pd.DataFrame(notebooks)
        
        # print(df_notebooks.head())
        df_notebooks.to_csv(self.KAGGLE_NOTEBOOK_LOG_FILE, mode = 'a', index=False)
        # ‘existing.csv’, mode=’a’, index=False, header=False
        # self.download_kernels
        return df_notebooks


# import kaggle 
# query = "cancer"
# kernel_list = kaggle.api.kernels_list(search = query, page=1)
# print(kernel_list)

if __name__ == '__main__':
    KERNEL_DOWNLOAD_PATH = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks/Kaggle')
    KAGGLE_NOTEBOOK_LOG_FILE = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks/Kaggle/kaggle_notebook_log.csv')
    QUERY_FILE = os.path.join(os.getcwd(), 'notebooksearch/Queries/kaggle_queries.csv')

    # Read queries
    # df_queries = pd.read_csv(QUERY_FILE)
    queries = ['cancer']
    df_queries = pd.DataFrame(queries, columns= ['queries'])
    # print(df_queries)

    crawler = KaggleNotebookCrawler(df_queries, KERNEL_DOWNLOAD_PATH, KAGGLE_NOTEBOOK_LOG_FILE)
    results = crawler.crawl_notebooks()
    # print(results)
