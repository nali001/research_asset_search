import requests
from pprint import pprint
import time

ONLINE_API_ENDPOINT = 'http://145.100.135.119/api/'
ONLINE_API_CONFIG = {
    'verify': False,
    'headers': {
        # "Accept": "*/*",
        # "Content-Type": "text/json",
        "Authorization": "Token 5901347bc7ccd4560fe687a3ec0754b26904ba6a", 
    }
}

LOCAL_API_ENDPOINT = 'http://127.0.0.1:7777/api/'
LOCAL_API_CONFIG = {
    'verify': False,
    'headers': {
        # "Accept": "*/*",
        # "Content-Type": "text/json",
        "Authorization": "Token ab132fc1bc7f55d8410d276335b5e922a7d60072", 
    }
}


# ----------------------------------------- Working ------------------------------
def initialize_app(api_endpoint): 
    ''' Initialize the web application
    '''
    url = api_endpoint + "initialize_app/"
    response = requests.get(url)
    print('------------------------ Result -----------------------\n')
    pprint(response.json())
    print('----------------------------------------------------------------------------\n')


def obatain_api_token(api_endpoint): 
    ''' Get api token for API calls
    '''
    url = api_endpoint + "obtain_api_token/"
    response = requests.get(url)
    print('------------------------ Token -----------------------\n')
    pprint(response.json())
    print('----------------------------------------------------------------------------\n')


def test_api_token(api_endpoint, api_config): 
    ''' Test api token
    '''
    url = api_endpoint
    response = requests.get(url, **api_config)
    print('------------------------ Welcome -----------------------\n')
    pprint(response.json())
    print('----------------------------------------------------------------------------\n')


def send_user_profile(api_endpoint, api_config):
    ''' Post userprofile data
    '''
    url = api_endpoint + "create_userprofile/"
    client_id = 'smalldog'
    research_interests = "machine learning"
    # event = 'notebook_search'
    # timestamp = str(time.time())
    # query = 'yes please'
    data = {
        "client_id": client_id, 
        "research_interests": research_interests, 
    }
    response = requests.post(url, json = data, **api_config)
    print('------------------------ Example of user feedback -----------------------\n')
    pprint(response.json())
    print('----------------------------------------------------------------------------\n')


def get_notebook_search(api_endpoint, api_config): 
    query = 'cancer'
    url = api_endpoint + "notebook_search/"
    params={
        "page": "1",
        "query": query,
        "filter": "",
        "facet": "",
    }
    response = requests.get(url, params=params, **api_config)
    hits = response.json()
    results = hits['results']
    # hits = response
    print('------------------------ First 10 of notebook results -----------------------\n')
    for i in range(10): 
        pprint(results[i]['name'])
    print('----------------------------------------------------------------------------\n')
    return hits

def post_notebook_search(api_endpoint, api_config):
    ''' test
    '''
    query = 'bird'
    url = api_endpoint + "notebook_search/"
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
    response = requests.post(url, params=params, data=data, **api_config)
    hits = response.json()
    results = hits['results']
    # hits = response
    print('------------------------ First 10 of notebook results -----------------------\n')
    for i in range(min(len(results), 10)): 
        pprint(results[i]['name'])
    print('----------------------------------------------------------------------------\n')
    return hits

# ------------------------------------------------------------------------------------


def test(api_endpoint, api_config):
    ''' test
    '''
    query = 'bread'
    url = api_endpoint + "test/"
    params={
        "page": "1",
        "query": query,
        "filter": "",
        "facet": "",
    }
    response = requests.get(url, params=params, **api_config)
    hits = response.json()['results']
    # hits = response
    print('------------------------ Example of searching result -----------------------\n')
    pprint(hits[0])
    print('----------------------------------------------------------------------------\n')
    return hits

if __name__ == "__main__": 
    # initialize_app(ONLINE_API_ENDPOINT)
    # obatain_api_token(ONLINE_API_ENDPOINT)
    # test_api_token(ONLINE_API_ENDPOINT, ONLINE_API_CONFIG)
    get_notebook_search(ONLINE_API_ENDPOINT, ONLINE_API_CONFIG)