import json
import os
from notebooksearch import notebook_crawling

class NotebookDownloader:
    def __init__(self): 
        pass 
    def get_notebook_by_docid(self, docid):
        print(f'\n\nCurrentttttt path :{os.getcwd()}\n\n')
        sample_file = os.path.join(os.getcwd(), 'notebooksearch/sample.ipynb')
        with open(sample_file, 'r') as f: 
            notebook_source_file = f.read()
        download_result = {
            'docid': docid, 
            'notebook_source_file': notebook_source_file
            } 
        return download_result