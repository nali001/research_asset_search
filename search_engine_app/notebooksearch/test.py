from notebooksearch import notebook_preprocessing
import json
import os
from notebooksearch.notebook_preprocessing import RawNotebookPreprocessor
# with open('notebooksearch/sample.ipynb') as f: 
#     notebook_json = json.load(f)

# contents = notebook_preprocessing.NotebookContents()
# lang = contents.extract_new_contents(notebook_json)
# print(lang)

input_path = os.path.join(os.getcwd(), 'notebooksearch/Raw_notebooks')
output_path = os.path.join(os.getcwd(), 'notebooksearch/Notebooks')
preprocessor = RawNotebookPreprocessor(input_path=input_path, output_path=output_path)
source_name='Kaggle'

# preprocessor.dump_raw_notebooks(source_name='Kaggle')
df_features = preprocessor.add_new_features(source_name='Kaggle')
print(df_features)