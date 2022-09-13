from elasticsearch_dsl import Index
import json
import os

from notebook_search import utils
from elasticsearch import Elasticsearch

def open_file(file):
    read_path = file
    with open(read_path, "r", errors='ignore') as read_file:
        data = json.load(read_file)
    return data
# ----------------------------------------------------------------
def index_notebooks(es: Elasticsearch, index_name: str, notebook_path: str) -> Elasticsearch:
    """ Feed the preprocessed notebooks into the index of Elasticsearch server named `index_name`

    Args:
        es: The connected Elasticsearch client 
        index_name: The name of the index to be created for indexing notebooks. 
        notebook_path: Directory for storing preprocessed notebooks

    """
    # es = utils.create_es_client()
    index = Index(index_name, es)

    if not es.indices.exists(index = index_name):
        index.settings(
            index={'mapping': {'ignore_malformed': True}}
        )
        index.create()
    else:
        es.indices.close(index=index_name)
        put = es.indices.put_settings(
            index=index_name,
            body={
                "index": {
                    "mapping": {
                        "ignore_malformed": True
                    }
                }
            })
        es.indices.open(index=index_name)
    cnt=0
    root = notebook_path
    for path, subdirs, files in os.walk(root):
        for name in files:
            cnt=cnt+1
            indexfile= os.path.join(path, name)
            indexfile = open_file(indexfile)
            newRecord={
                "name":indexfile["name"],
                "full_name":indexfile["full_name"],
                "stargazers_count":indexfile["stargazers_count"],
                "forks_count":indexfile["forks_count"],
                "description":indexfile["description"],
                "size":indexfile["size"],
                "language": indexfile["language"],
                "html_url":indexfile["html_url"],
                "git_url":indexfile["git_url"]
            }
            res = es.index(index=index_name, id = indexfile["git_url"], body=newRecord)
            es.indices.refresh(index=index_name)
            print(str(cnt)+" recode added! \n")
    return es
# ----------------------------------------------------------------

if __name__ == '__main__': 
    es = utils.create_es_client()
    index_notebooks(es, 'notebooks', os.getcwd() + 'Jupyter Notebook/')
# test()