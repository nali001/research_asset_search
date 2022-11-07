import os 
import time
import pandas as pd
import kaggle
import json
import tqdm


class NotebookCrawler: 
    pass


class KaggleNotebookCrawler: 
    METADATA_FILE_NAME = "kernel-metadata.json"

    def __init__(self, df_queries, KERNEL_DOWNLOAD_PATH, KAGGLE_DOWNLOAD_LOG_FILE, KAGGLE_SEARCH_LOG_FILE):
        self.KERNEL_DOWNLOAD_PATH = KERNEL_DOWNLOAD_PATH
        self.KAGGLE_DOWNLOAD_LOG_FILE = KAGGLE_DOWNLOAD_LOG_FILE
        self.KAGGLE_SEARCH_LOG_FILE = KAGGLE_SEARCH_LOG_FILE
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
            - Boolean: Only True when the file is correctly downloaded or already exists. 


        The notebook will be downloaded as 'dirname_basename' of `kernel_ref`. 

        For example, given kernel_ref = 'buddhiniw/breast-cancer-prediction', 
        there will be two files downloaded: 
            - buddhiniw_breast-cancer-prediction.ipynb
            - buddhiniw_breast-cancer-prediction.json
        '''
        download_path = self.KERNEL_DOWNLOAD_PATH
        file_name = os.path.dirname(kernel_ref) + '_' + os.path.basename(kernel_ref)

        # Check if the file is already downloaded
        if self.file_exists(file_name): 
            print(f'*** {kernel_ref} *** already exists!')
            return True
        
        try: 
            kaggle.api.kernels_pull(kernel_ref, download_path, metadata=True)
            print(f'[Pulling] {kernel_ref}')
            
            old_file_name = os.path.basename(kernel_ref)
            if not self.file_exists(old_file_name): 
                print(f'[***FAIL] {kernel_ref}')
                old_metadata = os.path.join(download_path, self.METADATA_FILE_NAME)

                # It is very important to delete the metadata file, otherwise the following downloading will fail
                os.remove(old_metadata)
                return False

            # Rename the notebook file
            try: 
                old_file = os.path.join(download_path, os.path.basename(kernel_ref)) + '.ipynb'
                new_file = os.path.join(download_path, file_name) + '.ipynb'
                os.rename(old_file, new_file)
            except FileNotFoundError as err: 
                print("Exception: ", err)
                return False

            # Rename the metadata file
            try: 
                old_metadata = os.path.join(download_path, self.METADATA_FILE_NAME)
                new_metadata = os.path.join(download_path, file_name) + '.json'
                os.rename(old_metadata, new_metadata)
            except FileNotFoundError as err:
                print("Exception: ", err)
                return False
        except Exception as err: 
            print("Exception: ", err)
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
        for i, query in tqdm(enumerate(df_queries['queries'])): 
            # To save the memory, we write the searching results to disk for every 10 queries 
            notebooks.extend(self.search_kernels(query, page_range))
            if i%10 == 0 or i == len(df_queries['queries']): 
                df_notebooks = pd.DataFrame(notebooks)
                # Delete duplicated results
                df_notebooks.drop_duplicates(inplace=True)

                # Update notebook search logs
                try: 
                    search_logs = pd.read_csv(self.KAGGLE_SEARCH_LOG_FILE)
                    search_all = search_logs.merge(df_notebooks, how='left')
                except: 
                    search_all = df_notebooks
                search_all.to_csv(self.KAGGLE_SEARCH_LOG_FILE, index=False)
                print(f'Saving searching results to disk...')
                # Reset the notebooks after saving to
                notebooks = []


        # Read notebook download logs and filter out the new notbooks to download
        try: 
            download_logs = pd.read_csv(self.KAGGLE_DOWNLOAD_LOG_FILE)
            download_all = df_notebooks.merge(download_logs.drop_duplicates(), how='left', indicator=True)
            new_notebooks = download_all[download_all['_merge'] == 'left_only'].drop(columns=['_merge'])
            download_all = download_all.drop(columns=['_merge'])
        except Exception as e:
            print(e) 
            new_notebooks = df_notebooks
            download_all = df_notebooks
        
        print(f'--------------------------- {len(new_notebooks)} new Notebooks --------------------------------')
        print(f'{new_notebooks}')
        print(f'----------------------------------------------------------------------------')
        
        # Download the notebooks and only keep record for downloaded notebooks 
        for kernel_ref in  tqdm(new_notebooks['kernel_ref']): 
            if not self.download_kernel(kernel_ref):
                download_all.drop(download_all[download_all['kernel_ref']==kernel_ref].index, inplace=True)

        # Save notebook names, IDs etc to .csv file. 
        download_all.to_csv(self.KAGGLE_DOWNLOAD_LOG_FILE, index=False)

        return True


def main(): 
    # Check if the current working path is `search_engine_app``, if not terminate the program
    if os.path.basename(os.getcwd()) != 'search_engine_app': 
        print(f'Please navigate to `search_engine_app` directory and run: \n `python -m notebooksearch.notebook_crawling`\n')
        return False

    KERNEL_DOWNLOAD_PATH = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks/Kaggle')
    KAGGLE_DOWNLOAD_LOG_FILE = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks/logs/kaggle_download_log.csv')
    KAGGLE_SEARCH_LOG_FILE = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks/logs/kaggle_search_log.csv')
    QUERY_FILE = os.path.join(os.getcwd(), 'notebooksearch/Queries/kaggle_crawler_queries.csv')

    # Read queries
    df_queries = pd.read_csv(QUERY_FILE)
    # queries = ['wsi']
    # df_queries = pd.DataFrame(queries, columns= ['queries'])
    # print(df_queries)

    crawler = KaggleNotebookCrawler(df_queries, KERNEL_DOWNLOAD_PATH, KAGGLE_DOWNLOAD_LOG_FILE, KAGGLE_SEARCH_LOG_FILE)
    result = crawler.crawl_notebooks(page_range=100)
    return result

if __name__ == '__main__':
    main()

