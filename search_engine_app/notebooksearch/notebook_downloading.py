import os
import pandas as pd
from notebooksearch import utils

class NotebookDownloader:
    def __init__(self): 
        pass
    def get_notebook_from_es(self, docid, index_name):
        es = utils.create_es_client()
        source = es.get_source(index=index_name, id=docid)
        result = {
            'docid': source['docid'], 
            'notebook_source_file': source['notebook_source_file']
        }
        return result

    def get_notebook_from_disk(self, docid, notebook_file): 
        notebook_path = os.path.join(os.getcwd(), notebook_file)
        df_notebooks = pd.read_csv(notebook_path)
        result = df_notebooks[df_notebooks['docid']==docid].to_dict('records')[0]
        result = {
            'docid': result['docid'], 
            'notebook_source_file': result['notebook_source_file']
        }
        return result