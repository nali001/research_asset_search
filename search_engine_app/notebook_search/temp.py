from datetime import datetime
# Only use import for packages and modules, not classes or functions. 
# Always use absolute path for importing modules even it is from the same package. 
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
from notebook_search import utils



es = utils.create_es_client()
q = Q("multi_match", query='ocean', fields=['name', 'description'])

s = Search(using = es, index = 'notebooks').query(q)
response = s.execute()

for hit in s:
    print(hit.name)


