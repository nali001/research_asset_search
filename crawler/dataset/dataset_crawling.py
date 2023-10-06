''' dataset_crawling.py
Crawl datasets from multiple web locations. 


'''

import os 
import json
from datetime import datetime
import pandas as pd
import itertools
import requests
import hashlib

import kaggle
import time
from datetime import timedelta
from memory_profiler import profile
 

class DatasetCrawler: 
    def __init__(self, source_name=None, df_queries=None, size=100, **kwargs):
        self.source_name = source_name
        self.df_queries = df_queries
        self.size=size
        self.identifier = None
        if self.source_name=='Zenodo': 
            self.identifier = 'doi'
        elif self.source_name=='Kaggle': 
            self.identifier = 'ref'
        elif self.source_name=='Dryad': 
            self.identifier = 'identifier'
        for key, value in kwargs.items(): 
            setattr(self, key, value) 
    
    @staticmethod
    def _search_zenodo_datasets(query=None, size=100):
        ''' Search for datasets in Zenodo using keyword queries. 
        Args: 
            - query: str. Keywrods for searching datasets
            - size: int. The number of returned datasets
        Return: 
            - hits: [{}]. Serializable dict of the returned dataset metadata records. 
        '''
        MAX_RETRIES = 5  # Maximum number of retries
        BASE_DELAY = 10  # Base delay in seconds for the first retry

        base_url = "https://zenodo.org/api/records/"
        params = {
            "q": query,
            "size": size,  # Number of results to retrieve, adjust as needed
            "type": "dataset",
        }
        
        retries = 0
        hits = []
        while retries < MAX_RETRIES:
            try:
                response = requests.get(base_url, params=params)

                if response.status_code == 500:
                    print("Server Error (HTTP 500). Skiping..")
                    return hits

                response.raise_for_status()  # Check for HTTP errors

                # Parse the JSON response
                data = response.json()
                hits = data.get("hits", {}).get("hits", [])
                break 

            except requests.exceptions.RequestException as e:
                print("Error:", e)

                # Increment retries and apply exponential backoff
                retries += 1
                if retries < MAX_RETRIES:
                    delay = BASE_DELAY * 2**retries
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print("Maximum retries reached. Unable to retrieve data.")

        return hits
    

    @staticmethod
    def _search_kaggle_datasets(query=None, size=100): 
        ''' Search for datasets in Kaggle using keyword queries. 
        Args: 
            - query: str. Keywrods for searching datasets
            - size: int. The number of returned datasets
        Return: 
            - hits: [{}]. Serializable dict of the returned dataset metadata records. 
        '''

        # Helper functions
        def convert_datetime(obj):
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            
        def serialize_data(data):
            ''' Transform dict data to JSON seriablizable'''
            return json.loads(json.dumps(data, default=convert_datetime))
        
        # Search for datasets
        page_range = size%10+1
        hits = []

        for page in range(1, page_range+1): 
            # retries = 0
            datasets = kaggle.api.dataset_list(search=query, page=page)
            print(f'Crawling page {page}')                
            
            if len(datasets) == 0: 
                break

            else: 
                for ds in datasets: 
                    ds_vars = vars(ds)
                    # Convert datetime values to string
                    serialized_data = serialize_data(ds_vars)
                    hits.append(serialized_data)

        return hits
    
    @staticmethod
    def _search_dryad_datasets(query=None, size=100): 
        ''' Search for datasets in Dryad using keyword queries. 
        Request example: https://datadryad.org/api/v2/search?page=1&per_page=100&q=link%20prediction
        Args: 
            - query: str. Keywrods for searching datasets
            - size: int. The number of returned datasets
        Return: 
            - hits: [{}]. Serializable dict of the returned dataset metadata records. 
        '''
        # Get token
        def get_dryad_token(credential_path): 
            with open(credential_path) as f:
                credential = json.load(f)
            url = "https://datadryad.org/oauth/token"
            client_id = credential["application_id"]
            client_secret = credential["secret"]
            grant_type = "client_credentials"

            payload = {
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": grant_type
            }

            headers = {
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
            }

            response = requests.post(url, data=payload, headers=headers)

            if response.status_code == 200:
                print("Token successfully retrieved:")
                print(response.json())
                
                # Save the access token to a JSON file
                access_token = response.json().get("access_token")
                token_data = {"access_token": access_token}

                current_date = datetime.now().strftime('%Y-%m-%d')
                output_path = os.path.join(os.path.dirname(credential_path), f'dryad_token_{current_date}.json')
                
                with open(output_path, "w") as json_file:
                    json.dump(token_data, json_file)
                print(f"Saved to {output_path}")
                
            else:
                print("Failed to retrieve token. Status code:", response.status_code)
                print("Response:", response.text)

            return access_token


        # Load token 
        file_path = os.path.join(os.getcwd(), "secrets/dryad_token.json")
        with open(file_path, "r") as json_file:
            access_token = json.load(json_file)["access_token"]
        
        # Create token
        # credential_path = os.path.join(os.getcwd(), 'secrets/dryad_client_credential.json')
        # access_token = get_dryad_token(credential_path=credential_path)
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Search for datasets
        api_url = "https://datadryad.org/api/v2/search"  # Replace with the actual API endpoint

        per_page = 100
        page_range = size%per_page+1
        hits = []

        for page in range(1, page_range+1): 
            params = {
            "q": query, 
            "per_page": per_page, 
            "page": page, 
            }
            try:
                response = requests.get(api_url, params=params, headers=headers)
                response.raise_for_status()  # Raise an exception for bad requests

                # Parse the JSON response
                data = response.json()
                datasets = data.get("_embedded", {}).get("stash:datasets", [])

                print(f'Crawling page {page}') 


            except requests.exceptions.RequestException as e: 
                if response.status_code == 403:
                    print("Error 403: Skipping this query.")
                    return hits
                else:
                    print("Error:", e)    

            if len(datasets) == 0: 
                break
            
            else: 
                hits.extend(datasets)
        return hits


    def search_datasets(self, query=None, size=100): 
        ''' Search datasets using given query
        Return: 
            - results: dict. The metadata records of returned datasets. 
        '''
        results = None
        if self.source_name=='Zenodo': 
            results = self._search_zenodo_datasets(query, size)
        elif self.source_name=='Kaggle': 
            results = self._search_kaggle_datasets(query, size)
        elif self.source_name=='Dryad': 
            results = self._search_dryad_datasets(query, size)
        return results
    

    def download_datasets(self, query=None, size=100):
        ''' Download the metadata files of the datasets given ONE query. 
        Calling the `search_datasets` within it and serialize all returned metatada records into JSON files. 
        '''
        # Search for datasets first
        results = self.search_datasets(query=query, size=size)
        logs = []

        # If there is no result
        if not results: 
            return pd.DataFrame(logs)
        
        download_path = self.DOWNLOAD_PATH
        for record in results: 
            try:
                file_id = record[self.identifier]
            except Exception as err: 
                print(err)
                print(record)
                raise err
            
            # Rename the dataset file using hash values
            print(file_id)
            file_name = 'DS_'+hashlib.sha256(file_id.encode('utf-8')).hexdigest()
            file_path = os.path.join(download_path, os.path.basename(file_name)) + '.json'
        
            # Check if the file is already downloaded
            if os.path.exists(file_path): 
                print(f'[!!EXIST] {file_id}')
                continue  

            try: 
                with open(file_path, 'w') as f_out: 
                    json.dump(record, f_out)
            except Exception as err: 
                print("Exception: ", err)
                continue

            logs.append({
                'query': query, 
                self.identifier: record[self.identifier]})
        
        return pd.DataFrame(logs)

    @staticmethod
    def _check_log(df, log_file, check_columns):
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
    
    @staticmethod
    def _update_log(df, log_file):
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
        pass

    # memory_profile decorator
    @profile
    def bulk_download(self, df_queries, size): 
        ''' Download a bunch of datasets using keywords'''

        df_queries = self.df_queries
        # Read dataset download logs and filter out the new queries to download
        temp = self._check_log(df_queries, self.DOWNLOAD_LOG_FILE, ['query'])
        # Then check the no record log, not to search for queries that do not have records
        new_queries = self._check_log(temp, self.DOWNLOAD_NO_RECORD_FILE, ['query'])

        print(f'--------------------------- {len(new_queries)} new Queries --------------------------------')
        print(f'{new_queries}')
        print(f'----------------------------------------------------------------------------\n\n')

        if new_queries.empty: 
            print(f'Seach task has been finished!')
            return True

        df_datasets = pd.DataFrame()
        df_no_records = pd.DataFrame()

        # Search datasets for each query
        start = time.time()
        for i, query in enumerate(new_queries['query']): 
            print(f'---------------- Query [{i+1}]: {query} ----------------')
            new_datasets = self.download_datasets(query, size)
        
            if new_datasets.empty: 
                no_record = pd.DataFrame.from_dict([{
                    'query': query, 
                    'no_record': True
                    }])
                df_no_records = pd.concat([df_no_records, no_record])
            
            df_datasets = pd.concat([df_datasets, new_datasets])
            df_datasets.drop_duplicates(inplace=True)

            # To save the memory, we write the searching results to disk for every 10 queries 
            if (i+1)%1 == 0 or i+1 == len(new_queries): 
                self._update_log(df_no_records, self.DOWNLOAD_NO_RECORD_FILE)
                # Update notebook search logs
                self._update_log(df_datasets, self.DOWNLOAD_LOG_FILE)
                end = time.time()
                print(f'>>>>> Saving {len(df_datasets)} searching results to disk...')
                print(f'>>>>> Time elapsed: {str(timedelta(seconds=int(end-start)))}\n\n')
                # Reset the notebooks after saving to the log file
                df_datasets.drop(df_datasets.index, inplace=True) 

        return True


    def crawl_datasets(self):
        ''' Search and download datasets using given queries 

        The dataset metadata files will be downloaded to disk
        '''
        if not os.path.isfile(self.DOWNLOAD_LOG_FILE): 
            pd.DataFrame(columns=['query', self.identifier]).to_csv(self.DOWNLOAD_LOG_FILE, index=False)
        # try: 
        #     df_queries = pd.read_csv(self.DOWNLOAD_LOG_FILE)['query']
        # except Exception as e:
        #     print(f'[DownloadLog ERROR(self-defined)] There is no download log file specified!') 
    
        self.bulk_download(df_queries=self.df_queries, size=self.size)
        return True


# --------------------------------- Usage examples

def crawl_PWC_datasets(source_name, QUERY_FILE, size, task=None): 
    '''
    Args: 
        - source_name: {'Zenodo', 'Kaggle', 'Dryad'}
    '''
    # Check if the current working path is `notebook_search_docker``, if not terminate the program
    if os.path.basename(os.getcwd()) != 'notebook_search_docker': 
        print(f'Please navigate to `notebook_search_docker` directory and run: \n `python -m crawler.dataset_crawling`\n')
        return False

    ROOT = os.path.join(os.getcwd(), f'data/dataset/{source_name}')
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
    
    # queries = ['link prediction']
    # df_queries = pd.DataFrame(queries, columns=['query'])
    # print(df_queries)

    kwargs = {
        'DOWNLOAD_PATH': DOWNLOAD_PATH, 
        'DOWNLOAD_LOG_FILE': DOWNLOAD_LOG_FILE, 
        'SEARCH_LOG_FILE': SEARCH_LOG_FILE, 
        'SEARCH_NO_RECORD_FILE': SEARCH_NO_RECORD_FILE, 
        'DOWNLOAD_NO_RECORD_FILE': DOWNLOAD_NO_RECORD_FILE
    }
    crawler = DatasetCrawler(source_name=source_name, df_queries=df_queries, size=size, **kwargs)


    if task=='search': 
        result = crawler.bulk_search(size=size)
    elif task=='crawl': 
        result = crawler.crawl_datasets()
    else: 
        return None
    return result




def main():
    # PWC_PATH = os.path.join(os.getcwd(), 'notebooksearch/Queries')
    # generate_pwc_queries(PWC_PATH)
    
    QUERY_FILE = os.path.join(os.getcwd(), 'data/Queries/pwc_queries.csv')
    tasks = ['crawl']
    for task in tasks: 
        crawl_PWC_datasets(source_name='Dryad', QUERY_FILE=QUERY_FILE, size=100, task=task)
        crawl_PWC_datasets(source_name='Dryad', QUERY_FILE=QUERY_FILE, size=100, task=task)
    return True

if __name__ == '__main__':
    main()

