from django.test import TestCase
import requests
from notebook_search import notebook_retrieval

import os

# test_notebook_path = os.path.join(os.getcwd(), 'tests/Jupyter Notebook')
# test_index_name = 'test-index'

class TestNotebookRetrieval(TestCase):
    def test_notebook_retrieval(self):
        """
        Test the returned results
        """
        r =requests.get('http://127.0.0.1:7777/notebook_search/genericsearch/?term=cancer&page=1')
        searcher = notebook_retrieval.Genericsearch(r)
        results = searcher.genericsearch()
        print(results)
        # self.assertTrue(es.indices.exists(index = test_index_name), 'Indexing pipeline passed test.')
        # es.indices.delete(index = test_index_name)
