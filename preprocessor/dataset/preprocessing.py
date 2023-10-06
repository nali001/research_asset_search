''' preprocessor.dataset.preprocessing.py
Preprocess dataset metadata form various respositories. 

- input: {data_dir}/{self.source_name}/{self.query_source}/,
- output: {data_dir}/{self.source_name}/preprocessed_{self.preprocess_type}/{self.query_source}/, 
'''

import os
import json
import glob
from datetime import datetime

from utils import utils
from .metadata_mappings import ZENODO_MATADATA_MAPPING
from .metadata_mappings import KAGGLE_METADATA_MAPPING
from .metadata_mappings import DRYAD_CONTENT_MAPPING
from .metadata_mappings import DRYAD_LICENSES


class DatasetMetadataPreprocessor:
    def __init__(self, source_name: str, query_source: str, preprocess_type:str):
        '''
        Args: 
            - preprocess_type: {'basic'}
        '''
        self.source_name = source_name
        self.query_source = query_source
        self.preprocess_type = preprocess_type
        self.preprocessors = {
            'basic': self._basic_preprocess, 
        }
        self.mapping_rules = {
            'Zenodo': ZENODO_MATADATA_MAPPING, 
            'Kaggle': KAGGLE_METADATA_MAPPING, 
            'Dryad': DRYAD_CONTENT_MAPPING, 
        }

        data_dir = os.path.join(utils.get_data_dir())

        self.directories = {
            'input': f'{data_dir}/{self.source_name}/{self.query_source}/',
            'output': f'{data_dir}/{self.source_name}/'
                    f'preprocessed_{self.preprocess_type}/{self.query_source}/', 
        }

        for d in self.directories.values():
            os.makedirs(d, exist_ok=True)

        print(f"Input: {self.directories['input']}")
        print(f"Ouput: {self.directories['output']}\n")

    
    @staticmethod
    def _convert_bits_to_human_readable(value_in_bits):
        # Define the conversion factors
        KB = 1024  # 1 kilobyte = 1024 bits
        MB = KB * KB  # 1 megabyte = 1024 kilobytes
        GB = MB * KB  # 1 gigabyte = 1024 megabytes

        if value_in_bits < KB:
            return f"{value_in_bits}bits"
        elif value_in_bits < MB:
            return f"{value_in_bits / KB:.1f}KB"
        elif value_in_bits < GB:
            return f"{value_in_bits / MB:.1f}MB"
        else:
            return f"{value_in_bits / GB:.1f}GB"

    def _get_size(self, dataset_metadata): 
        ''' Get the dataset size. '''
        size = '0bits'

        if self.source_name=='Zenodo':
            file_size_bits = 0
            for file in dataset_metadata['files']: 
                file_size_bits = file_size_bits + file['size'] 
            size = self._convert_bits_to_human_readable(file_size_bits)

        elif self.source_name=='Kaggle': 
            size = dataset_metadata['size']

        elif self.source_name=='Dryad': 
            file_size_bits = dataset_metadata['storageSize']
            size = self._convert_bits_to_human_readable(file_size_bits)
        
        else: 
            print("Error: Data source not supported.")
            
        return size
    
    def _get_last_updated(self, dataset_metadata):
        ''' Get the last_updated date for datasets. '''
        last_updated = ''

        if self.source_name=='Zenodo':
            datetime_str = dataset_metadata['updated']
            # Convert the string to a datetime object
            datetime_obj = datetime.fromisoformat(datetime_str)
            # Format the datetime object as a date string (e.g., '2023-08-09')
            last_updated = datetime_obj.strftime('%Y-%m-%d')

        elif self.source_name=='Kaggle': 
            datetime_str = dataset_metadata['lastUpdated']
            # Convert the string to a datetime object
            datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            # Format the datetime object as a date string (e.g., '2017-05-01')
            last_updated = datetime_obj.strftime('%Y-%m-%d')

        elif self.source_name=='Dryad': 
            last_updated = dataset_metadata['lastModificationDate']
        
        else: 
            print("Error: Data source not supported.")
            
        return last_updated



    def bulk_preprocess(self):
        ''' Read all the files from the input dir and process each accrodingly. 
        '''
        filename_pattern = os.path.join(self.directories['input'], '*.json')
        for i, filename in enumerate(glob.glob(filename_pattern)):
            basename = os.path.basename(filename)
            docid = os.path.splitext(basename)[0]

            try: 
                with open(filename) as f:
                    dataset_metadata = json.load(f)
                    # Add some fields to dataset metadata
                    dataset_metadata['docid'] = docid
                    dataset_metadata['source'] = self.source_name
                    dataset_metadata['size'] = self._get_size(dataset_metadata)
                    dataset_metadata['last_updated'] = self._get_last_updated(dataset_metadata)
                    # We need to process the license info in Dryad datasets
                    if self.source_name == 'Dryad': 
                        license_url = dataset_metadata['license']
                        dataset_metadata['license'] = DRYAD_LICENSES[license_url]
                        # print(dataset_metadata['license'])
                        # break
            except: 
                continue
            
            output_filename = os.path.join(self.directories['output'], basename)

            # Call the preprocess function for each file
            if self.preprocess(dataset_metadata, output_filename): 
                print(f"{[i+1]} datasets preprocessed!")
                
    
    def preprocess(self, dataset_metadata: dict, output_filename: str):
        ''' Switch to the correct preprocessing method using `preprocess_type` indicator. 
        '''
        preprocess_method = self.preprocessors.get(self.preprocess_type, self._default_preprocess)
        
        preprocess_method(dataset_metadata, output_filename)
        return True
        
    def _default_preprocess(self):
        pass

        
    def _basic_preprocess(self, dataset_metadata: dict, output_filename: str):
        """
        :param dataset_metadata: Dataset metadata
        :param output_filename: Path to the output metadata (json)
        :return:
        """
        # base_result = self._base_preprocess(notebook, notebook_metadata)
        
        # Map the data 
        mapping_rule = self.mapping_rules.get(source_name)
        summary_doc = utils.map_metadata(dataset_metadata, mapping_rule)

        with open(output_filename, 'w') as f:
            json.dump(summary_doc, f)

if __name__ == '__main__': 
    ''' Usage: python -m preprocessor.dataset.preprocessing
    '''
    # Prepare data: {DATA_DIR}/{source_name}/raw_notebooks/{docid}.json
    # Prepare data: {DATA_DIR}/{source_name}/raw_notebooks/{docid}.ipynb
    os.environ['DATA_DIR'] = './data/dataset'
    source_name = 'Zenodo'
    # source_name = 'Kaggle'
    # source_name = 'Dryad'
    query_source = 'PWC'
    preprocess_type = 'basic'
    preprocessor = DatasetMetadataPreprocessor(source_name=source_name, query_source=query_source, preprocess_type=preprocess_type)
    preprocessor.bulk_preprocess()
    