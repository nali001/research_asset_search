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
        "Authorization": "Token ab132fc1bc7f55d8410d276335b5e922a7d60072", 
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
    user_id = 'bigface'
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



def notebook_search_test():
    url = API_ENDPOINT + "notebook_search_test/"
    user_id = 'bigface'
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

def send_user_info():
    url = API_ENDPOINT + "create_user/"
    client_id = 'bigface'
    # event = 'notebook_search'
    # timestamp = str(time.time())
    # query = 'yes please'
    data = {
        "client_id": client_id, 
    }
    response = requests.post(url, data = data, **POST_CONFIG)
    print('------------------------ Example of user feedback -----------------------\n')
    pprint(response.json())
    print('----------------------------------------------------------------------------\n')

def send_user_profile():
    url = API_ENDPOINT + "create_userprofile/"
    client_id = 'smalldog'
    client_user = {
        "client_id": client_id, 
    }
    research_interests = "machine learning"
    # event = 'notebook_search'
    # timestamp = str(time.time())
    # query = 'yes please'
    data = {
        "client_id": client_id, 
        "research_interests": research_interests, 
    }
    response = requests.post(url, json = data, **POST_CONFIG)
    print('------------------------ Example of user feedback -----------------------\n')
    pprint(response.json())
    print('----------------------------------------------------------------------------\n')



if __name__ == "__main__": 
    send_user_profile()