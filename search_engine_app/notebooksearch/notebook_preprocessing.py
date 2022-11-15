import os
import json
import pandas as pd
from tqdm import tqdm

from notebooksearch import utils

class RawNotebookPreprocessor:
    ''' A class for handling raw notebooks. 
    
    Args: 
        - input_path: The path of a folder under which the .ipynb files reside. 
        - output_path: The path of a folder where the .csv files will be placed. 
    '''
    def __init__(self, input_path:str, output_path:str) -> bool: 
        self.input_path = input_path
        self.output_path = output_path
    # def generate_docid(self, notebooks): 
    #     notebooks['docid'] = range(len(notebooks))

    # def docid2filename(self, source_name:str, docid:str):
    #     if source_name == 'Kaggle': 
    #         pass 

    # def filename2docid(self): 
    #     pass

    def dump_raw_notebooks(self, source_name:str):
        ''' Dump raw notebooks to a .csv file. 

        And keep a record of notebook metadata in another .csv file
        '''
        root = os.path.join(self.input_path, source_name)
        raw_notebooks = []
        # Go through all the .ipynb file and store the contents in one single .csv file. 
        for path, _, files in os.walk(root):
            for name in files:
                if name.endswith('.ipynb'): 
                    file_path = os.path.join(path, name)
                    notebook = utils.read_json_file(file_path)
                    notebook = json.dumps(notebook)

                    # Read metadata
                    metadata_path = os.path.join(path, name[:-6]+'.json')
                    metadata = utils.read_json_file(metadata_path)
                    new_record = {
                        "source_id": metadata['id'], 
                        "source_name": source_name, 
                        "file_name": name, 
                        "notebook_source_file": notebook
                        }
                    raw_notebooks.append(new_record)
                else: 
                    continue
        df_raw_notebooks = pd.DataFrame.from_dict(raw_notebooks)
        df_raw_notebooks['docid'] = range(len(df_raw_notebooks))
        df_raw_notebooks['docid'] = df_raw_notebooks['docid'].apply(lambda x: source_name + str(x))
        print(f'Number of raw notebooks: {len(df_raw_notebooks)}\n')

        df_metadata = df_raw_notebooks.drop(columns=['notebook_source_file'])
        output_dir = self.output_path

        # Save the resulting files
        notebook_file = os.path.join(output_dir, source_name + '_raw_notebooks.csv')
        metadata_file = os.path.join(output_dir, source_name + '_notebook_metadata.csv')

        print(f'Saving raw notebooks to: {notebook_file}\n')
        df_raw_notebooks.to_csv(notebook_file, index=False)

        print(f'Saving notebook metadata to: {metadata_file}\n')
        df_metadata.to_csv(metadata_file, index=False)

    def add_new_notebooks(self): 
        ''' Add new raw notebooks to existent records. 
        '''
        pass

    
def main():
    input_path = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks')
    output_path = input_path
    preprocessor = RawNotebookPreprocessor(input_path=input_path, output_path=output_path)
    preprocessor.dump_raw_notebooks(source_name='Kaggle')


if __name__ == '__main__': 
    main()