from django.test import TestCase

from notebook_search import notebook_indexing
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q

import os

test_notebook_path = os.path.join(os.getcwd(), 'tests/Jupyter Notebook')
test_index_name = 'test-index'

class TestNotebookIndexing(TestCase):
    def test_notebook_indexing(self):
        """
        Test that it can sum a list of integers
        """
        es = notebook_indexing.index_notebooks(test_index_name, test_notebook_path)
        # s = Search(using = es, index = 'test-index')
        # q = Q("multi_match", query='ocean', fields=['title', 'body'])
        # s.query(q)
        # es.get(index = 'test-index')
        self.assertTrue(es.indices.exists(index = test_index_name), 'Indexing pipeline passed test.')
        es.indices.delete(index = test_index_name)
