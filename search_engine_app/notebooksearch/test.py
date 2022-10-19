from elasticsearch_dsl.query import MultiMatch, Match
from notebooksearch import utils
from elasticsearch_dsl import Search, Q
es = utils.create_es_client()
# {"multi_match": {"query": "python django", "fields": ["title", "body"]}}
a = MultiMatch(query='python django', fields=['name', 'descriptions'])

# {"match": {"title": {"query": "web framework", "type": "phrase"}}}
b = Match(title={"query": "web framework", "type": "phrase"})

s = Search(using=es)
