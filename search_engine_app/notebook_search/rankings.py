from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

ELASTICSEARCH_HOSTNAMES = ["elasticsearch", "localhost"]
# ELASTICSEARCH_HOSTNAMES = ["elasticsearch", "localhost"]

# Try different host names for Elasticsearch service. 
# It depends on on what machine the service is running. 
for host in ELASTICSEARCH_HOSTNAMES: 
    es = Elasticsearch(
        hosts=[{"host": host, "port": 9200}],
        http_auth=["elastic", "changeme"],
        )
    if es.ping(): 
        break


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