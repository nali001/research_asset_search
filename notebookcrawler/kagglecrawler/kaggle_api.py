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

    def download_kernel(self, kernel_ref): 
        if '/' in kernel_ref:
            dataset_urls = kernel_ref.split('/')
            owner_slug = dataset_urls[0]
            kernel_slug = dataset_urls[1]

        response = kaggle.api.process_response(
            kaggle.api.kernel_pull_with_http_info(owner_slug, kernel_slug))
        return response


    def search_kernels(self, query, page_range): 
        kernels = []
        for page in range(1, page_range+1): 
            kernel_list = []
            try: 
                kernel_list = kaggle.api.kernels_list(search=query, page=page)
                print(f'Crawling page {page}') 
                # Add sleep here to prevent `TooMany Requests`` error
                time.sleep(5)               
                if len(kernel_list) == 0: 
                    break
                else: 
                    kernels.extend(kernel_list)
            # Skip the pages that cause ApiException
            except kaggle.rest.ApiException as e:  
                print(e)
                continue
    
        # Extract the `title` and the `ref` of returned Kaggle kernels
        results = []
        for kernel in kernels:
            results.append({
                'query': query, 
                'title': kernel.title, 
                'kernel_ref': kernel.ref})
        return results

