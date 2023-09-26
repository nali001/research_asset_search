from .ner import EntityExtractor
from elasticsearch.helpers import scan
from utils import utils

class QueryReformulator: 
    def __init__(self, object_type=None, docid=None, index_name=None): 
        self.object_type = object_type
        self.docid = docid
        self.index_name = index_name
    
    def extract_entities_from_notebook(self):
        # Get the contents using docid
        # Assuming df_notebook contains the notebook content for the given docid
        content = self._get_notebook_content(self.docid, self.index_name)  # You'll need to implement this function

        # Extract entities
        extractor = EntityExtractor(content_type='text', model_name='xxx')
        entities = extractor.extract_entities(content)
        return entities
    
    def reformulate_query_for_notebook(self, query=None): 
        entities = self.extract_entities_from_notebook()
        non_none_values = [value for key, value in entities.items() if value is not None]
        reformed_query = query + ' ' + ' '.join(non_none_values)
        return reformed_query
    
    # Replace this with actual implementation of getting notebook content based on docid
    @staticmethod
    def _get_notebook_content(docid, index_name):
        query = {
            "query": {
                "match": {
                    "docid": docid
                }
            }
        }
        es = utils.create_es_client()
        # Use a scan to retrieve all matching documents
        search_results = scan(es, query=query, index=index_name)

        # Process the results
        for hit in search_results:
            notebook_content = hit['_source']['description']
            break
        return notebook_content


# ------------------------------------------------
def main():
    query = "Point cloud"
    reformulator = QueryReformulator(object_type='notebook', docid='NB_3303738aff8da496ae1366dd059d0343ddcb5eedd8e3c0c92209bac6caa97d0d', index_name='notebook_online')
    reformed = reformulator.reformulate_query_for_notebook(query=query)
    print(f"-------------- Reformed query ------------\n{reformed}")
    print("-------------------------------------------\n")

# python -m ir.query_reformulation
if __name__ == '__main__': 
    main()