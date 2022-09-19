import requests

def get_notebook_search_results(): 
    keyword = 'cancer'
    response = requests.get(
        'http://127.0.0.1:7777/api/notebook_search/',
        params={
            "page": "1",
            "keywords": keyword,
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
    print(hits)
    return hits

if __name__ == "__main__": 
    get_notebook_search_results()