from webbrowser import get
import requests
from pprint import pprint
import time

# API_ENDPOINT = 'http://145.100.135.119/api/'
API_ENDPOINT = 'http://127.0.0.1:7777/api/'
API_CONFIG = {
    'verify': False,
    'headers': {
        # "Accept": "*/*",
        # "Content-Type": "text/json",
        "Authorization": "Token ab132fc1bc7f55d8410d276335b5e922a7d60072", 
    }
}

# ----------------------------------------- Working ------------------------------
def send_user_profile():
    ''' Post userprofile data
    '''
    url = API_ENDPOINT + "create_userprofile/"
    client_id = 'smalldog'
    research_interests = "machine learning"
    # event = 'notebook_search'
    # timestamp = str(time.time())
    # query = 'yes please'
    data = {
        "client_id": client_id, 
        "research_interests": research_interests, 
    }
    response = requests.post(url, json = data, **API_CONFIG)
    print('------------------------ Example of user feedback -----------------------\n')
    pprint(response.json())
    print('----------------------------------------------------------------------------\n')



def get_notebook_search(): 
    query = 'cancer'
    url = API_ENDPOINT + "notebook_search/"
    params={
        "page": "1",
        "query": query,
        "filter": "",
        "facet": "",
    }
    response = requests.get(url, params=params, **API_CONFIG)
    hits = response.json()
    results = hits['results']
    # hits = response
    print('------------------------ First 10 of notebook results -----------------------\n')
    for i in range(10): 
        pprint(results[i]['name'])
    print('----------------------------------------------------------------------------\n')
    return hits

def post_notebook_search():
    ''' test
    '''
    query = 'bird'
    url = API_ENDPOINT + "notebook_search/"
    params = {
        "page": "1",
        "query": query,
        "filter": "",
        "facet": "",
    }

    client_id = 'applepie'
    event = "notebook_search"
    data = {
        "client_id": client_id, 
        "timestamp": str(time.time()), 
        "event": event, 
        "query": query, 
    }
    response = requests.post(url, params=params, data=data, **API_CONFIG)
    hits = response.json()
    results = hits['results']
    # hits = response
    print('------------------------ First 10 of notebook results -----------------------\n')
    for i in range(min(len(results), 10)): 
        pprint(results[i]['name'])
    print('----------------------------------------------------------------------------\n')
    return hits

# ------------------------------------------------------------------------------------


def test():
    ''' test
    '''
    query = 'bread'
    url = API_ENDPOINT + "test/"
    params={
        "page": "1",
        "query": query,
        "filter": "",
        "facet": "",
    }
    response = requests.get(url, params=params, **API_CONFIG)
    hits = response.json()['results']
    # hits = response
    print('------------------------ Example of searching result -----------------------\n')
    pprint(hits[0])
    print('----------------------------------------------------------------------------\n')
    return hits

if __name__ == "__main__": 
    post_notebook_search()