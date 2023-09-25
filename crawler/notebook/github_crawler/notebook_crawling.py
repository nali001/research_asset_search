''' notebook_crawling.py
Crawl notebooks from Kaggle. 
18 Sep 2023 checking notes: It seems that this is only for crawling notebooks from Kaggle, not from Github. 
Each item contains a .ipynb source file and a .json metadata file. 

'''

import os 
import pandas as pd

import requests
import kaggle
import time
from datetime import timedelta
from memory_profiler import profile
 



class GithubNotebookCrawler: 
    def __init__(self, df_queries, num_repos=100, **kwargs):
        self.df_queries = df_queries
        for key, value in kwargs.items(): 
            setattr(self, key, value) 

    def search_repos(self, query): 
        ''' Given one query, search Github repositories with the language Jupyter Notebook. 
        '''
        # GitHub search API endpoint
        api_url = 'https://api.github.com/search/repositories'
       
        search_query = f'{query} language:Jupyter Notebook'  # Modify this based on your search criteria

        repositories = []
        # Send a request to the GitHub search API
        response = requests.get(api_url, params={'q': search_query}) 
        # Check if the request was successful
        if response.status_code == 200:
            # Extract repository information from the response
            repositories = response.json().get('items', []) 
        else:
            print('Failed to search for Jupyter notebooks. Status code:', response.status_code)
        
        return repositories
    

    def download_notebooks(self, repo_full_name):
        ''' Download notebooks from one repository. 
        Args: 
            - repo_full_name: str/str. 
        '''
        repo_contents_url = f'{self.github_api_url}/{repo_full_name}/contents'
        notebook_count = 0

        response = requests.get(repo_contents_url)

        if response.status_code == 200:
            repo_contents = response.json()

            for content in repo_contents:
                if content['type'] == 'file' and content['name'].endswith('.ipynb'):
                    notebook_response = requests.get(content['download_url'])

                    if notebook_response.status_code == 200:
                        notebook_content = notebook_response.content

                        repo_directory = repo_full_name.replace('/', '_')
                        os.makedirs(repo_directory, exist_ok=True)
                        notebook_filename = f'{content["name"]}'
                        notebook_path = os.path.join(repo_directory, notebook_filename)

                        with open(notebook_path, 'wb') as notebook_file:
                            notebook_file.write(notebook_content)

                        print(f'Downloaded {notebook_filename} from {repo_full_name}')
                        notebook_count += 1

            print(f'Total Jupyter notebooks downloaded from {repo_full_name}: {notebook_count}\n')

        else:
            print(f'Failed to retrieve contents of {repo_full_name}. Status code:', response.status_code)


        
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
        '''' Search for notebooks given a set of queries. '''
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


# ----------------------------

def crawl_PWC_notebooks(source_name, QUERY_FILE, size, task=None): 
    # Check if the current working path is `notebook_search_docker``, if not terminate the program
    if os.path.basename(os.getcwd()) != 'notebook_search_docker': 
        print(f'Please navigate to `notebook_search_docker` directory and run: \n `python -m crawler.dataset_crawling`\n')
        return False

    ROOT = os.path.join(os.getcwd(), f'data/notebook/{source_name}')
    DOWNLOAD_PATH = os.path.join(ROOT, 'PWC')
    LOG_PATH = os.path.join(ROOT, 'PWC_logs')
    DOWNLOAD_LOG_FILE = os.path.join(LOG_PATH, 'pwc_download_log.csv')
    SEARCH_LOG_FILE = os.path.join(LOG_PATH, 'pwc_search_log.csv')
    SEARCH_NO_RECORD_FILE = os.path.join(LOG_PATH, 'pwc_search_no_record.csv')
    DOWNLOAD_NO_RECORD_FILE = os.path.join(LOG_PATH, 'pwc_download_no_record.csv')

    os.makedirs(ROOT, exist_ok=True)
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)
    os.makedirs(LOG_PATH, exist_ok=True)

    # Read queries
    df_queries = pd.DataFrame(pd.read_csv(QUERY_FILE)['query'])
    # queries = ['wsi']
    # df_queries = pd.DataFrame(queries, columns=['query'])
    # print(df_queries)
    kwargs = {
        'DOWNLOAD_PATH': DOWNLOAD_PATH, 
        'DOWNLOAD_LOG_FILE': DOWNLOAD_LOG_FILE, 
        'SEARCH_LOG_FILE': SEARCH_LOG_FILE, 
        'SEARCH_NO_RECORD_FILE': SEARCH_NO_RECORD_FILE, 
        'DOWNLOAD_NO_RECORD_FILE': DOWNLOAD_NO_RECORD_FILE
    }
    crawler = GithubNotebookCrawler(source_name=source_name, df_queries=df_queries, size=size, **kwargs)


    if task=='search': 
        result = crawler.bulk_search(size=size)
    elif task=='crawl': 
        result = crawler.crawl_notebooks()
    else: 
        return None
    return result




def main():
    # PWC_PATH = os.path.join(os.getcwd(), 'notebooksearch/Queries')
    # generate_pwc_queries(PWC_PATH)
    
    QUERY_FILE = os.path.join(os.getcwd(), 'data/Queries/pwc_queries.csv')
    tasks = ['crawl']
    for task in tasks: 
        crawl_PWC_notebooks(source_name='Github', QUERY_FILE=QUERY_FILE, num_repos=100, task=task)
        crawl_PWC_notebooks(source_name='Github', QUERY_FILE=QUERY_FILE, num_repos=100, task=task)
    return True

if __name__ == '__main__':
    main()


