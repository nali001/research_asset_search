import requests
from pprint import pprint
import time

# API_ENDPOINT = 'http://145.100.135.119/api/'
API_ENDPOINT = 'http://127.0.0.1:7777/api/'
POST_CONFIG = {
    'verify': False,
    'headers': {
        # "Accept": "*/*",
        # "Content-Type": "text/json",
        "Authorization": "Token 6d0bd0aeb32a5bad4da35ebab477c7abb65213cf"
    }
}

def get_notebook_search_results(): 
    term = 'bread'
    response = requests.get(
        'http://145.100.135.119/api/notebook_search/',
        params={
            "page": "1",
            "term": term,
            "filter": "",
            "facet": ""
        }, 
        verify=False,
        headers={
            "Accept": "*/*",
            "Content-Type": "text/json",
            "Authorization": "Token b30bd18ea01f5a45e217b03682f70ce6ae14c293"
        }
    )
    hits = response.json()
    # hits = response
    print('------------------------ Example of searching result -----------------------\n')
    pprint(hits[7])
    print('----------------------------------------------------------------------------\n')
    return hits

def notebook_search_test():
    url = API_ENDPOINT + "notebook_search_test/"
    user_id = 'klm2022'
    event = 'notebook_search'
    timestamp = str(time.time())
    query = 'yes please'
    data = {
        "user_id": user_id, 
        "event": event, 
        "timestamp": timestamp, 
        "query": query, 
    }
    print(data)
    response = requests.post(url, data = data, **POST_CONFIG)
    print('------------------------ Example of user feedback -----------------------\n')
    pprint(response.json())
    print('----------------------------------------------------------------------------\n')

if __name__ == "__main__": 
    notebook_search_test()