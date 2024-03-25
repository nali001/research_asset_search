from elasticsearch.helpers import scan
from utils import utils
import os
import json
from itertools import chain
from .ner import EntityExtractor


class QueryReformulator: 
    def __init__(self, object_type=None, docid=None, index_name_list=None): 
        self.object_type = object_type
        self.docid = docid
        self.index_name_list = index_name_list
    
    def extract_entities_from_notebook(self):
        # Get the contents using docid
        # Assuming df_notebook contains the notebook content for the given docid
        content = self._get_notebook_content(self.docid, self.index_name_list)  # You'll need to implement this function
        # content = nb['description']
        if content=='': 
            print(f'[[{os.getcwd()}]] No description: {self.docid}')
            entities = {}
        else: 
            # Extract entities
            extractor = EntityExtractor(content_type='text', model_name='chatgpt')
            entities = extractor.extract_entities(content)

        return entities
    
    def reformulate_query_for_notebook(self, query=None): 
        entities = self.extract_entities_from_notebook()
        entities = json.loads(entities)
        non_none_values = [] 
        def list_entities(value):
            if isinstance(value, list):
                for k in value:
                    list_entities(k)        
            else:
                non_none_values.append(value)
        for key, value in entities.items():
            if bool(value):
                list_entities(value)
            else:
                entities[key] = 'N/A'
        
        reformed_query = query + ' ' + ' '.join(non_none_values)
        
        entities.update({"reformed_query": reformed_query})

        print(entities)
        
        # return reformed_query
        return entities
    
    # Replace this with actual implementation of getting notebook content based on docid
    @staticmethod
    def _get_notebook_content(docid, index_name_list):
        query = {
            "query": {
                "match": {
                    "docid": docid
                }
            }
        }
        es = utils.create_es_client()
        # Use a scan to retrieve all matching documents
        search_results = scan(es, query=query, index=index_name_list)

        # Process the results
        for hit in search_results:
            # print(hit)
            notebook_content = hit['_source']['description']
            break

        return notebook_content


# ------------------------------------------------
def main():
    query = "Point cloud"
    # reformulator = QueryReformulator(object_type='notebook', docid='NB_93a306f0bd0e6567dfa1afcc01f0f985fafa0b4d156fabace1c99a6b584b4e7e', index_name='notebook_online')
    reformulator = QueryReformulator(object_type='notebook', docid='NB_b7e8217d45d41b10a9754adfeef5c62b779bc1fd83aa48eb7f8c9d117a8ce55d', index_name='notebook_online')
    reformed = reformulator.reformulate_query_for_notebook(query=query)
    print(f"-------------- Reformed query ------------\n{reformed}")
    print("-------------------------------------------\n")

# python -m ir.query_reformulation
if __name__ == '__main__': 
    main()