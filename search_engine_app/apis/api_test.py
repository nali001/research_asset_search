from lib2to3.pgen2.pgen import generate_grammar
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
    data = {
        "client_id": client_id, 
        "research_interests": research_interests, 
    }
    response = requests.post(url, json = data, **api_config)
    print('------------------------ Example of user feedback -----------------------\n')
    pprint(response.json())
    print('----------------------------------------------------------------------------\n')


def get_notebook_search(api_endpoint, api_config): 
    query = 'question'
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
    print('------------------------ First 10 of notebook results -----------------------\n')
    for i in range(10): 
        pprint(results[i]['name'])
    print('----------------------------------------------------------------------------\n')
    print('------------------------------ Result fields ---------------------------\n')
    pprint(results[0].keys())
    print('----------------------------------------------------------------------------\n')
    return hits

def post_notebook_search(api_endpoint, api_config):
    ''' test notebook search with `POST` method
    '''
    query = 'bird'
    url = api_endpoint + "notebook_search/"
    params = {
        "page": "1",
        "query": query,
        "filter": "",
        "facet": "",
    }

    client_id = 'sugar'
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
    print('------------------------ First 10 of notebook results -----------------------\n')
    for i in range(min(len(results), 10)): 
        pprint(results[i]['name'])
    print('----------------------------------------------------------------------------\n')
    return hits

def query_generation(api_endpoint, api_config): 
    ''' test query generation API with `POST` method
    '''
    url = api_endpoint + "query_generation/"
    client_id = 'kitten'
    event = "query_generation"
    cell_contents = [
        {
            "cell_type": "markdown",
            "cell_content": "Great", 
        }, 
        {
            "cell_type": "markdown",
            "cell_content": "Mamammia", 
        }, 
        ]
    data = {
        "client_id": client_id, 
        "timestamp": str(time.time()), 
        "event": event, 
        "cell_contents": cell_contents, 
    }
    response = requests.post(url, json=data, **api_config)
    results = response.json()
    print('------------------------ Generated quries results -----------------------\n')
    pprint(results)
    print('----------------------------------------------------------------------------\n')
    return results


def context_search(api_endpoint, api_config):
    ''' test context_based search API with `POST` method
    '''
    # Get generated queries via calling query_generation API
    generated_queries = query_generation(api_endpoint, api_config)

    # Modify `POST` data
    generated_queries["event"] = "context_search"
    generated_queries["timestamp"] = str(time.time())
    query = 'recall'
    data = {**generated_queries, **{"query": query}}

    # print(data)
    print('------------------------ Modified data -----------------------\n')
    pprint(data)
    print('----------------------------------------------------------------------------\n')
    

    # Send request to context search API
    url = api_endpoint + "context_search/"
    params = {
        "page": "1",
        "query": query,
        "filter": "",
        "facet": "",
    }
    response = requests.post(url, params=params, json=data, **api_config)
    hits = response.json()
    results = hits['search_results']['results']
    print('------------------------ First 10 of notebook results -----------------------\n')
    for i in range(10): 
        pprint(results[i]['name'])
    print('----------------------------------------------------------------------------\n')
    return hits


def relevancy_feedback(api_endpoint, api_config): 
    ''' test query generation API with `POST` method
    '''
    url = api_endpoint + "relevancy_feedback/"
    client_id = 'Old man never lies'
    event = "relevancy_feedback"
    query = "what do you think about powerpoint?"
    num_stars = 4
    hits = get_notebook_search(api_endpoint, api_config)
    notebook = hits["results"][0]
    annotated_notebook = {}
    for attr in ['docid', 'name', 'source', 'html_url', 'description']: 
        annotated_notebook[attr] = notebook[attr]
        
    data = {
        "client_id": client_id, 
        "timestamp": str(time.time()), 
        "event": event, 
        "query": query, 
        "num_stars": str(num_stars), 
        "annotated_notebook": annotated_notebook, 
    }
    response = requests.post(url, json=data, **api_config)
    # results = response.json()
    print('------------------------ User feedback -----------------------\n')
    pprint(response.status_code)
    print('----------------------------------------------------------------------------\n')
    return True
# ------------------------------------------------------------------------------------


def test(api_endpoint, api_config):
    pass



if __name__ == "__main__": 
    # initialize_app(ONLINE_API_ENDPOINT)
    # obatain_api_token(ONLINE_API_ENDPOINT)
    # test_api_token(LOCAL_API_ENDPOINT, LOCAL_API_CONFIG)
    # get_notebook_search(LOCAL_API_ENDPOINT, LOCAL_API_CONFIG)
    # post_notebook_search(LOCAL_API_ENDPOINT, LOCAL_API_CONFIG)
    # query_generation(LOCAL_API_ENDPOINT, LOCAL_API_CONFIG)
    # context_search(LOCAL_API_ENDPOINT, LOCAL_API_CONFIG)
    relevancy_feedback(LOCAL_API_ENDPOINT, LOCAL_API_CONFIG)

