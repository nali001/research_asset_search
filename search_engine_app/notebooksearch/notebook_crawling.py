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

    def search_kernels(self, query, page_range): 
        ''' Search Kaggle kernels using given query
        '''
        print(f'------------- Query: {query} -------------')
        kernels = []
        for page in range(1, page_range+1): 
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
                'kernel_ref': kernel.ref})
        
        print('\n')
        return results

    def download_kernel(self, kernel_ref):
        ''' Download the kernels together with the metadata file

        Args: 
            - kernel_ref: the ID used by Kaggle to denote one notebook. 
        
        Return: 
            - Boolean: Only True when everything is correct. 


        The notebook will be downloaded as 'dirname_basename' of `kernel_ref`. 

        For example, given kernel_ref = 'buddhiniw/breast-cancer-prediction', 
        there will be two files downloaded: 
            - buddhiniw_breast-cancer-prediction.ipynb
            - buddhiniw_breast-cancer-prediction.json
        '''
        download_path = self.KERNEL_DOWNLOAD_PATH
        file_name = os.path.dirname(kernel_ref) + '_' + os.path.basename(kernel_ref)

        # Check if the file already downloaded
        if self.file_exists(file_name): 
            print(f'*** {kernel_ref} *** already exists!')
            return False
        
        try: 
            kaggle.api.kernels_pull(kernel_ref, download_path, metadata=True)
            print(f'Downloaded *** {kernel_ref} ***')
        except Exception as err: 
            print("Exception: ", err)
            return False
        
        # Rename the notebook
        try: 
            old_notebook = os.path.join(download_path, os.path.basename(kernel_ref)) + '.ipynb'
            new_notebook = os.path.join(download_path, file_name) + '.ipynb'
            os.rename(old_notebook, new_notebook)
        except FileNotFoundError:
            return False


        # Rename the metadata file
        try: 
            old_metadata = os.path.join(download_path, self.METADATA_FILE_NAME)
            new_metadata = os.path.join(download_path, file_name) + '.json'
            os.rename(old_metadata, new_metadata)
        except FileNotFoundError:
            return False

        return True

    def file_exists(self, file_name): 
        file_path = os.path.join(self.KERNEL_DOWNLOAD_PATH, file_name) + ".ipynb" 
        if os.path.exists(file_path): 
            return True
        else: 
            return False
        
    def has_results(kernel_list): 
        if len(kernel_list) == 0:
            return False
        else: 
            return True   

    def crawl_notebooks(self, page_range):
        ''' Search and download notebooks using given queries 
        '''
        df_queries = self.df_queries
        notebooks = []

        # Search notebooks for each query
        for query in df_queries['queries']: 
            notebooks.extend(self.search_kernels(query, page_range))
        df_notebooks = pd.DataFrame(notebooks)

        # Delete duplicated results
        df_notebooks.drop_duplicates(inplace=True)

        # Read notebook logs and filter out the new notbooks to download
        try: 
            notebook_logs = pd.read_csv(self.KAGGLE_NOTEBOOK_LOG_FILE)
            df_all = df_notebooks.merge(notebook_logs.drop_duplicates(), how='left', indicator=True)
            new_notebooks = df_all[df_all['_merge'] == 'left_only'].drop(columns=['_merge'])
            df_all = df_all.drop(columns=['_merge'])
            print(f'---------------------- New Notebooks -----------------------\n{new_notebooks}\n')
        except: 
            new_notebooks = df_notebooks
            df_all = df_notebooks
        
        # Download the notebooks
        for kernel_ref in new_notebooks['kernel_ref']: 
            self.download_kernel(kernel_ref)

        # Save notebook names, IDs etc to .csv file. 
        df_all.to_csv(self.KAGGLE_NOTEBOOK_LOG_FILE, index=False)

        return True



if __name__ == '__main__':
    KERNEL_DOWNLOAD_PATH = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks/Kaggle')
    KAGGLE_NOTEBOOK_LOG_FILE = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks/logs/kaggle_notebook_log.csv')
    QUERY_FILE = os.path.join(os.getcwd(), 'notebooksearch/Queries/kaggle_queries.csv')

    # Read queries
    # df_queries = pd.read_csv(QUERY_FILE)
    queries = ['cancer']
    df_queries = pd.DataFrame(queries, columns= ['queries'])
    # print(df_queries)

    crawler = KaggleNotebookCrawler(df_queries, KERNEL_DOWNLOAD_PATH, KAGGLE_NOTEBOOK_LOG_FILE)
    results = crawler.crawl_notebooks(page_range=100)
