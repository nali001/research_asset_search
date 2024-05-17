from notebooksearch import utils
es = utils.create_es_client()

if __name__ == '__main__': 
    print(es.indices.get_alias())