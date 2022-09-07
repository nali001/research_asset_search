from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
es = Elasticsearch(
    hosts=[{"host": "elasticsearch", "port": 9200}],
    http_auth=["elastic", "changeme"],
)

# es_index_client = IndicesClient(es_client)
# es_index_client.create(index="laptops-demo")

doc = {
    'author': 'author_name',
    'text': 'Interensting content...',
    'timestamp': datetime.now(),
}
resp = es.index(index="test-index", id=1, body=doc)

resp = es.get(index="test-index", id=1)

print('Done')
