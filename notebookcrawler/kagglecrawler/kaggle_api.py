# kaggle_api.py
# This is an authentication Kaggle API

import json
import kaggle
import time
from kaggle import KaggleApi



class AuthenticatedKaggleAPI: 
    def __init__(self):
        kaggle_api = KaggleApi()
        # This requires th credenticial beding placed in '~/.kaggle/kaggle.json'
        kaggle_api.authenticate() 

    def download_kernel(self, kernel_ref:str) -> dict: 
        ''' Download one kernel 
        Args: 
            - kernel_ref: str. the same as Kaggle ID. 

        Return: 
            - response: responses from Kaggle.
            
        '''
        response = {}
        if '/' in kernel_ref:
            dataset_urls = kernel_ref.split('/')
            owner_slug = dataset_urls[0]
            kernel_slug = dataset_urls[1]

        for attempt in range(10): 
            try: 
                response = kaggle.api.process_response(
                    kaggle.api.kernel_pull_with_http_info(owner_slug, kernel_slug))
            # Capture the customized Exception. 
            # Execption definition: https://github.com/Kaggle/kaggle-api/blob/49057db362903d158b1e71a43d888b981dd27159/kaggle/rest.py#L311
            except kaggle.rest.ApiException as e:  
                # Sleep if it is due to 409 error. 
                if e.status==429: 
                    print(f'[ERROR!!] (429) {e.reason}')
                    retry_after = int(e.headers['Retry-After'])*20
                    print(f'\nRetry {attempt+1} in {retry_after} seconds zzzzZZZZZZ\n')
                    time.sleep(retry_after)
                    continue
                # Skip other exceptions
                else: 
                    break
        return response


    def search_kernels(self, query:str, page_range:int) -> list:
        ''' search `page_range` pages for one query 
        Args: 
            - 

        Return: 
            - result: a list of dict
        ''' 

        kernels = []
        for page in range(1, page_range+1): 
            end_page = False
            for attempt in range(10): 
                kernel_list = []
                try: 
                    # send request to Kaggle API
                    kernel_list = kaggle.api.kernels_list(search=query, page=page)
                    print(f'Crawled page {page}') 
                    
                    # Search until the end the result page               
                    if len(kernel_list) == 0: 
                        end_page = True

                    # Add sleep here to alleviate `TooMany Requests`` error
                    time.sleep(5)

                    # break from attempts if succeed. 
                    break 

                # Capture the customized Exception. 
                # Execption definition: https://github.com/Kaggle/kaggle-api/blob/49057db362903d158b1e71a43d888b981dd27159/kaggle/rest.py#L311
                except kaggle.rest.ApiException as e:  
                    # Sleep if it is due to 409 error. 
                    if e.status==429: 
                        print(f'[ERROR!!] (429) {e.reason}')
                        retry_after = int(e.headers['Retry-After'])*20
                        print(f'\nRetry {attempt+1} in {retry_after} seconds zzzzZZZZZZ\n')
                        time.sleep(retry_after)
                        continue
                    # Skip other exceptions
                    else: 
                        break

            # Stop searching until the end the result page               
            if end_page: 
                break
            else: 
                kernels.extend(kernel_list)
    
        # Extract the `title` and the `ref` of returned Kaggle kernels
        results = []
        if kernels: 
            for kernel in kernels:
                results.append({
                    'query': query, 
                    'title': kernel.title, 
                    'kernel_ref': kernel.ref})
        return results

