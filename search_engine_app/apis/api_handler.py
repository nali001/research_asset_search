import requests
from pprint import pprint

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

if __name__ == "__main__": 
    get_notebook_search_results()