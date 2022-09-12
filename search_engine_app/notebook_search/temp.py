from datetime import datetime
# Only use import for packages and modules, not classes or functions. 
# Always use absolute path for importing modules even it is from the same package. 
from notebook_search import utils


es = utils.create_es_client()

print(es.indices.get_alias())
