''' preprocessor.preprocessing.py
Preprocess notebooks form both Kaggle and Github using common metadata schema. 

- input: {data_dir}/{self.source_name}/raw_notebooks/,
- output_summary: preprocessed_{self.preprocess_type}/notebooks_summaries/, 
- output_contents: preprocessed_{self.preprocess_type}/notebooks_contents/, 

'''

import os
import json
import glob

from . import utils
from .notebook_statistics import NotebookStatistics
from .notebook_contents import NotebookContents
from .notebook_metadata import NotebookMetadata
from .metadata_mappings import COMMON_CONTENT_MAPPING


class RawNotebookPreprocessor:
    def __init__(self, source_name: str, preprocess_type: str):
        self.source_name = source_name
        self.preprocess_type = preprocess_type

        self.preprocessors = {
            'index': self._index_preprocess,
            'content': self._content_preprocess
        }    

        data_dir = os.path.join(utils.get_data_dir())


        self.directories = {
            'input': f'{data_dir}/{self.source_name}/raw_notebooks/',
            'output_summary': f'{data_dir}/{self.source_name}/'
                              f'preprocessed_{self.preprocess_type}/notebooks_summaries/', 
            'output_contents': f'{data_dir}/{self.source_name}/'
                               f'preprocessed_{self.preprocess_type}/notebooks_contents/', 
        }

        for d in self.directories.values():
            os.makedirs(d, exist_ok=True)

        
        
        print(f"Input: {self.directories['input']}")
        print(f"Summary: {self.directories['output_summary']}")
        print(f"Contents: {self.directories['output_contents']}\n")


    def bulk_preprocess(self):
        filename_pattern = os.path.join(self.directories['input'], '*.ipynb')
        for i, filename in enumerate(glob.glob(filename_pattern)):
            try: 
                with open(filename) as f:
                    notebook = json.load(f)
                with open(filename[:-6] + '.json') as f:
                    notebook_metadata = json.load(f)
            except: 
                continue
            basename = os.path.basename(filename)
            basename = os.path.splitext(basename)[0] + '.json'
            
            summary_filename = os.path.join(self.directories['output_summary'], basename)

            contents_filename = os.path.join(self.directories['output_contents'], basename)

            if self.preprocess(notebook, notebook_metadata, summary_filename, contents_filename): 
                print(f"{[i+1]} notebooks preprocessed!")
                
    
    def preprocess(self, notebook: dict, notebook_metadata: dict,
                   summary_filename: str, contents_filename: str):

        preprocess_method = self.preprocessors.get(self.preprocess_type, self.default_preprocess)
                
        preprocess_method(
            notebook,
            notebook_metadata,
            summary_filename,
            contents_filename
            )
        return True
        
    def default_preprocess(self):
        pass

    def _base_preprocess(self, notebook: dict, notebook_metadata: dict): 
        try:
            extracted_contents = NotebookContents(notebook).get_contents()
        except Exception as e:
            print(e)
            return

        try:
            statistics = NotebookStatistics(notebook).get_statistics()
        except Exception as e:
            print(e)
            return
        
        metadata = NotebookMetadata(self.source_name, notebook_metadata).get_metadata()
        contents = {**extracted_contents, **statistics}
        return {
            'metadata': metadata, 
            'contents': contents
        }
    
        
    def _index_preprocess(self, notebook: dict, notebook_metadata: dict,
                   summary_filename: str, contents_filename: str):
        """

        :param notebook: Notebook contents (parsed .ipynb)
        :param notebook_metadata: Notebook metadata
        :param summary_filename: Path to the output notebook summary (json)
        :param contents_filename: Path to the output notebook contents (json)
        :return:
        """
        base_result = self._base_preprocess(notebook, notebook_metadata)
        metadata = base_result['metadata']
        
        contents = base_result['contents']
        # Map the contents to common content schema
        common_contents = NotebookMetadata.map_metadata(contents, COMMON_CONTENT_MAPPING)
        
        summary_doc = {**metadata, **common_contents}

        contents_doc = summary_doc.copy()
        contents_doc["notebook_source_file"] = json.dumps(notebook)

        with open(summary_filename, 'w') as f:
            json.dump(summary_doc, f)

        with open(contents_filename, 'w') as f:
            json.dump(contents_doc, f)



    def _content_preprocess(self, notebook: dict, notebook_metadata: dict,
                   summary_filename: str, contents_filename: str):
        """

        :param notebook: Notebook contents (parsed .ipynb)
        :param notebook_metadata: Notebook metadata
        :param summary_filename: Path to the output notebook summary (json)
        :param contents_filename: Path to the output notebook contents (json)
        :return:
        """
        base_result = self._base_preprocess(notebook, notebook_metadata)
        if base_result is None: 
            print(f"None result for notebook {notebook_metadata['docid']}")
            return

        metadata = base_result['metadata']
        contents = base_result['contents']

        # Map the contents to common content schema
        common_contents = NotebookMetadata.map_metadata(contents, COMMON_CONTENT_MAPPING)
        
        summary_doc = {**metadata, **common_contents}

        contents_doc = {**metadata, **contents}

        with open(summary_filename, 'w') as f:
            json.dump(summary_doc, f)

        with open(contents_filename, 'w') as f:
            json.dump(contents_doc, f)


if __name__ == '__main__': 
    # Prepare data: {DATA_DIR}/{source_name}/raw_notebooks/{docid}.json
    # Prepare data: {DATA_DIR}/{source_name}/raw_notebooks/{docid}.ipynb
    os.environ['DATA_DIR'] = './data/notebook'
    source_name = 'Kaggle'
    preprocess_type = 'content'
    preprocessor = RawNotebookPreprocessor(source_name=source_name, preprocess_type=preprocess_type)
    preprocessor.bulk_preprocess()
    