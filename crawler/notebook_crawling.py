import os 
import json
import pandas as pd
import itertools

import kaggle
import time
from datetime import timedelta
from memory_profiler import profile
 

class PwcResource: 
    def __init__(self):
        ''' Handle the resources provided by paperwithcodes. 
        '''
        self.methods = None
        self.datasets = None
        self.tasks = None

    def get_methods(self, method_file):
        ''' Extract method names
        '''
        pwc_methods = []
        with open(method_file) as f: 
            methods = json.load(f) 

        for method in methods: 
            pwc_methods.append(method['name'])
            pwc_methods.append(method['full_name'])
        pwc_methods = list(set(pwc_methods))
        return pwc_methods

    def get_datasets(self, dataset_file):
        ''' Extract dataset names and task names'''
        pwc_datasets = []
        pwc_tasks = []
        with open(dataset_file) as f: 
            datasets = json.load(f) 

        for dataset in datasets: 
            pwc_datasets.append(dataset['name'])
            pwc_datasets.append(dataset['full_name'])
            if 'tasks' in dataset.keys(): 
                for task in dataset['tasks']:
                    pwc_tasks.append(task['task'])
            else: 
                continue
        
        pwc_datasets = list(set(pwc_datasets))
        pwc_tasks = list(set(pwc_tasks))
        return pwc_datasets, pwc_tasks
        
    def get_resources(self, file_path):
        method_file = os.path.join(file_path, 'methods.json')
        dataset_file = os.path.join(file_path, 'datasets.json')

        self.methods = self.get_methods(method_file)
        self.datasets, self.tasks = self.get_datasets(dataset_file)
        return self



class KaggleNotebookCrawler: 
    METADATA_FILE_NAME = "kernel-metadata.json"
    def __init__(self, df_queries, **kwargs):
        self.df_queries = df_queries
        for key, value in kwargs.items(): 
            setattr(self, key, value) 

    def search_kernels(self, query, page_range): 
        ''' Search Kaggle kernels using given query
        '''
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
        return pd.DataFrame(results)

    def download_kernel(self, kernel_ref):
        ''' Download the kernels together with the metadata file

        Args: 
            - kernel_ref: the ID used by Kaggle to denote one notebook. 
        
        Return: 
            - Boolean: Only True when the file is correctly downloaded or already exists. 
                If False, there are usaully something wrong with the Kaggle server or Kaggle API. 


        The notebook will be downloaded as 'dirname_basename' of `kernel_ref`. 

        For example, given kernel_ref = 'buddhiniw/breast-cancer-prediction', 
        there will be two files downloaded: 
            - buddhiniw_breast-cancer-prediction.ipynb
            - buddhiniw_breast-cancer-prediction.json
        '''
        download_path = self.DOWNLOAD_PATH
        try: 
            file_name = os.path.dirname(kernel_ref) + '_' + os.path.basename(kernel_ref)
        except Exception as e: 
            return False
            
        # Check if the file is already downloaded
        if self.file_exists(file_name): 
            print(f'[!!EXIST] {kernel_ref}')
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
        file_path = os.path.join(self.DOWNLOAD_PATH, file_name) + ".ipynb" 
        if os.path.exists(file_path): 
            return True
        else: 
            return False
        
    def has_results(self, kernel_list): 
        if len(kernel_list) == 0:
            return False
        else: 
            return True   

    def check_log(self, df, log_file, check_columns):
        ''' Check the log and return new records NOT contained in the log. 
        Args: 
            - df: DataFrame. 
            - log: DataFrame. 
            `df` and `log` should share the same scheme. 

        Return:
            - new_records: DataFrame. 
        '''
        try: 
            df_log = pd.read_csv(log_file)
        except Exception as e:
            print(e) 
            df_log = pd.DataFrame(columns=df.columns)
        
        merged = df.merge(df_log, how='left', on=check_columns, indicator=True, suffixes=['', '_DROP'])
        # new_records = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])

        drop_columns = [col for col in merged.columns if '_DROP' in col]
        new_records = merged[merged['_merge'] == 'left_only'][df.columns]
        new_records.reset_index(inplace=True, drop=True)
        return new_records

    def update_log(self, df, log_file):
        ''' Insert records that are not in the log file. ''' 
        try: 
            df_log = pd.read_csv(log_file)
        except Exception as e:
            print(e) 
            df_log = pd.DataFrame(columns=df.columns)

        if df.empty: 
            df_all = df_log
        else: 
            df_all = df_log.merge(df, how='outer')
        df_all.drop_duplicates(inplace=True)

        df_all.to_csv(log_file, index=False)
        return df_all

    # memory_profile decorator
    @profile
    def bulk_search(self, page_range): 
        '''' Search for notebooks '''
        df_queries = self.df_queries
        # Read notebook search logs and filter out the new notbooks to download
        temp = self.check_log(df_queries, self.SEARCH_LOG_FILE, ['query'])
        # Then check the no record log, not to search for queries that do not have records
        new_queries = self.check_log(temp, self.SEARCH_NO_RECORD_FILE, ['query'])

        print(f'--------------------------- {len(new_queries)} new Queries --------------------------------')
        print(f'{new_queries}')
        print(f'----------------------------------------------------------------------------\n\n')

        if new_queries.empty: 
            print(f'Seach task has been finished!')
            return True

        df_notebooks = pd.DataFrame()
        df_no_records = pd.DataFrame()
        # Search notebooks for each query
        start = time.time()
        for i, query in enumerate(new_queries['query']): 
            print(f'---------------- Query [{i+1}]: {query} ----------------')
            df_notebooks = pd.concat([df_notebooks, self.search_kernels(query, page_range)])
            df_notebooks.drop_duplicates(inplace=True)
            
            if df_notebooks.empty: 
                no_record = pd.DataFrame.from_dict([{
                    'query': query, 
                    'no_record': True
                    }])
                df_no_records = pd.concat([df_no_records, no_record])

            # To save the memory, we write the searching results to disk for every 10 queries 
            if (i+1)%10 == 0 or i+1 == len(new_queries): 
                self.update_log(df_no_records, self.SEARCH_NO_RECORD_FILE)
                # Update notebook search logs
                search_all = self.update_log(df_notebooks, self.SEARCH_LOG_FILE)
                end = time.time()
                print(f'>>>>> Saving {len(df_notebooks)} searching results to disk...')
                print(f'>>>>> Time elapsed: {str(timedelta(seconds=int(end-start)))}\n\n')
                # Reset the notebooks after saving to the log file
                df_notebooks.drop(df_notebooks.index, inplace=True) 
        return search_all

    # memory_profile decorator
    @profile
    def bulk_download(self, df_notebooks): 
        ''' Download a bunch of notebooks specified inside `df_notebooks`'''
        # Read notebook download logs and filter out the new notbooks to download
        temp = self.check_log(df_notebooks, self.DOWNLOAD_LOG_FILE, ['kernel_ref'])
        # Then check the no record logs to eliminate kernel_ref that has been failed to download. 
        new_notebooks = self.check_log(temp, self.DOWNLOAD_NO_RECORD_FILE, ['kernel_ref'])
        print(f'--------------------------- {len(new_notebooks)} new Notebooks --------------------------------')
        print(f'{new_notebooks}')
        print(f'----------------------------------------------------------------------------\n\n')

        # Download the notebooks and keep track of downloaded notebooks 
        start = time.time()
        downloaded_notebooks = pd.DataFrame()
        df_no_records = pd.DataFrame()
        print(f'------------------ {0} - {49}  notebooks -------------------')
        for j in range(len(new_notebooks)): 
            # Download the notebooks
            kernel_ref = new_notebooks.iloc[j]['kernel_ref']
            if self.download_kernel(kernel_ref):
                downloaded_notebooks = pd.concat([downloaded_notebooks, new_notebooks.iloc[[j]]])
            else:  
                no_record = pd.DataFrame.from_dict([{
                    'kernel_ref': kernel_ref, 
                    'no_record': True
                    }])
                df_no_records = pd.concat([df_no_records, no_record])


            if (j+1)%50==0 or j+1==len(new_notebooks): 
                # Update notebook download logs for every 100 notebooks
                self.update_log(df_no_records, self.DOWNLOAD_NO_RECORD_FILE)
                download_all = self.update_log(downloaded_notebooks, self.DOWNLOAD_LOG_FILE)
                end = time.time()
                print(f'\n\n>>>>> Saving {len(downloaded_notebooks)} downloaded results to disk...')
                print(f'>>>>> Time elapsed: {str(timedelta(seconds=int(end-start)))}\n\n')
                # Reset downloaded_notebooks
                downloaded_notebooks.drop(downloaded_notebooks.index, inplace=True) 
                print(f'------------------ {j+1} - {j+50}  notebooks -------------------')

        return True


    def crawl_notebooks(self, page_range, re_search=False):
        ''' Search and download notebooks using given queries 

        The notebooks will be downloaed to disk
        '''
        if re_search==True: 
            df_notebooks = self.bulk_search(page_range)
        else: 
            try: 
                df_notebooks = pd.read_csv(self.SEARCH_LOG_FILE)
            except Exception as e:
                print(f'[SearchLog ERROR(self-defined)] There is no search log file specified!') 
        
        self.bulk_download(df_notebooks)
        return True


# --------------------------------- Usage examples
def generate_pwc_queries(PWC_PATH): 
    ''' Generate queries for crawler using methods, datasets and tasks from PWC
    '''
    pwc = PwcResource()
    pwc.get_resources(PWC_PATH)
    methods = {'query': pwc.methods, 'type': ['method']*len(pwc.methods)}
    datasets = {'query': pwc.datasets, 'type': ['dataset']*len(pwc.datasets)}
    tasks = {'query': pwc.tasks, 'type': ['task']*len(pwc.tasks)}
    print(f'------------------ PWC resources -------------------')
    print(f'methods: {len(pwc.methods)}\ndatasets: {len(pwc.datasets)}\ntasks: {len(pwc.tasks)}\n')

    pwc_queries = {}
    for key in ['query', 'type']: 
        pwc_queries[key] = list(itertools.chain(methods[key], datasets[key], tasks[key]))
    df_pwc_queries = pd.DataFrame.from_dict(pwc_queries)
    
    # Save df_pwc_queries
    print(f'Save methods, dataset, tasks to `{PWC_PATH}/pwc_queries.csv`\n')
    df_pwc_queries.to_csv(os.path.join(PWC_PATH, 'pwc_queries.csv'), index=False)
    return df_pwc_queries

def crawl_kaggle_notebooks(QUERY_FILE, page_range, task=None, re_search=False): 
    # Check if the current working path is `search_engine_app``, if not terminate the program
    if os.path.basename(os.getcwd()) != 'search_engine_app': 
        print(f'Please navigate to `search_engine_app` directory and run: \n `python -m notebooksearch.notebook_crawling`\n')
        return False

    DOWNLOAD_PATH = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks/PWC/')
    DOWNLOAD_LOG_FILE = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks/PWC_logs/pwc_download_log.csv')
    SEARCH_LOG_FILE = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks/PWC_logs/pwc_search_log.csv')
    SEARCH_NO_RECORD_FILE = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks/PWC_logs/pwc_search_no_record.csv')
    DOWNLOAD_NO_RECORD_FILE = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks/PWC_logs/pwc_download_no_record.csv')

    # Read queries
    df_queries = pd.DataFrame(pd.read_csv(QUERY_FILE)['query'])
    # queries = ['wsi']
    # df_queries = pd.DataFrame(queries, columns= ['queries'])
    # print(df_queries)
    kwargs = {
        'DOWNLOAD_PATH': DOWNLOAD_PATH, 
        'DOWNLOAD_LOG_FILE': DOWNLOAD_LOG_FILE, 
        'SEARCH_LOG_FILE': SEARCH_LOG_FILE, 
        'SEARCH_NO_RECORD_FILE': SEARCH_NO_RECORD_FILE, 
        'DOWNLOAD_NO_RECORD_FILE': DOWNLOAD_NO_RECORD_FILE
    }
    crawler = KaggleNotebookCrawler(df_queries, **kwargs)


    if task=='search': 
        result = crawler.bulk_search(page_range=page_range)
    elif task=='crawl': 
        result = crawler.crawl_notebooks(page_range=page_range, re_search=re_search)
    else: 
        return None
    return result


def crawl_kaggle_notebooks_for_collected_queries(QUERY_FILE, page_range, task=None, re_search=False):
    ''' Crawl notebooks from Kaggle for collected queries. 
    ''' 
    # Check if the current working path is `search_engine_app``, if not terminate the program
    if os.path.basename(os.getcwd()) != 'search_engine_app': 
        print(f'Please navigate to `search_engine_app` directory and run: \n `python -m notebooksearch.notebook_crawling`\n')
        return False

    DOWNLOAD_PATH = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks/collected_queries/')
    DOWNLOAD_LOG_FILE = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks/collected_queries_logs/download_log.csv')
    SEARCH_LOG_FILE = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks/collected_queries_logs/search_log.csv')
    SEARCH_NO_RECORD_FILE = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks/collected_queries_logs/search_no_record.csv')
    DOWNLOAD_NO_RECORD_FILE = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks/collected_queries_logs/download_no_record.csv')

    # Read queries
    df_queries = pd.DataFrame(pd.read_csv(QUERY_FILE)['query'])
    # queries = ['wsi']
    # df_queries = pd.DataFrame(queries, columns= ['queries'])
    # print(df_queries)
    kwargs = {
        'DOWNLOAD_PATH': DOWNLOAD_PATH, 
        'DOWNLOAD_LOG_FILE': DOWNLOAD_LOG_FILE, 
        'SEARCH_LOG_FILE': SEARCH_LOG_FILE, 
        'SEARCH_NO_RECORD_FILE': SEARCH_NO_RECORD_FILE, 
        'DOWNLOAD_NO_RECORD_FILE': DOWNLOAD_NO_RECORD_FILE
    }
    crawler = KaggleNotebookCrawler(df_queries, **kwargs)


    if task=='search': 
        result = crawler.bulk_search(page_range=page_range)
    elif task=='crawl': 
        result = crawler.crawl_notebooks(page_range=page_range, re_search=re_search)
    else: 
        return None
    return result



def main():
    # PWC_PATH = os.path.join(os.getcwd(), 'notebooksearch/Queries')
    # generate_pwc_queries(PWC_PATH)
    
    QUERY_FILE = os.path.join(os.getcwd(), 'data/Queries/collected_queries.csv')
    tasks = ['search', 'crawl']
    for task in tasks: 
        crawl_kaggle_notebooks_for_collected_queries(QUERY_FILE, page_range=10, task=task, re_search=False)
        crawl_kaggle_notebooks_for_collected_queries(QUERY_FILE, page_range=10, task=task, re_search=False)
    return True

if __name__ == '__main__':
    main()

