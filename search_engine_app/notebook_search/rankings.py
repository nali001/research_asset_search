from utils import create_es_client

es = create_es_client()

# es_index_client = IndicesClient(es_client)
# es_index_client.create(index="laptops-demo")

doc = {
    'author': 'author_name',
    'text': 'Interensting content...',
    'timestamp': datetime.now(),
}
resp = es.index(index="test-index", id=1, body=doc)
# print(resp['result'])
resp = es.get(index="test-index", id=1)
# print(resp['_source'])

def elastic_test():
    return resp['_source']