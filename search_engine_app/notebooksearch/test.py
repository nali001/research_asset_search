from notebooksearch import utils
es = utils.create_es_client()
content = es.get_source(index='kaggle_notebooks', id='lnhtrang/single-cell-patterns')
print(content)