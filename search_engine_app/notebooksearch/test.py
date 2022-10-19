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


# def get_notebook_search(): 
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
print('------------------------ Example of searching result -----------------------\n')
for i in range(10): 
    print(results[i]["name"])
print('----------------------------------------------------------------------------\n')
    # return hits
