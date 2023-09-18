'''
change_filenames.py
Change the .ipynb and .json files downloaded from Kaggle to `docid`. 

'''

import os
import json
import hashlib

class FileRenamer:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.file_pairs = []
        self.json_files = []
        self.ipynb_files = []
    
    def generate_docid(self, html_url):
        docid = 'NB_' + hashlib.sha256(html_url.encode('utf-8')).hexdigest()
        return docid
    
    def collect_file_pairs(self):
        for file_name in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, file_name)
            
            if file_name.endswith('.json'):
                self.json_files.append(file_name)
            elif file_name.endswith('.ipynb'):
                self.ipynb_files.append(file_name)
        
        self.json_files.sort()
        self.ipynb_files.sort()
        
        if len(self.json_files) == len(self.ipynb_files):
            self.file_pairs = zip(self.json_files, self.ipynb_files)
        else:
            print("Number of JSON files and IPYNB files does not match.")
    
    def rename_files(self):
        for json_file, ipynb_file in self.file_pairs:
            json_path = os.path.join(self.folder_path, json_file)
            ipynb_path = os.path.join(self.folder_path, ipynb_file)
            
            with open(json_path, 'r') as json_file:
                data = json.load(json_file)
                html_url = "https://www.kaggle.com/code/" + data.get('id')
                if html_url:
                    docid = self.generate_docid(html_url)
                    
                    new_json_file = docid + '.json'
                    new_json_path = os.path.join(self.folder_path, new_json_file)
                    os.rename(json_path, new_json_path)

                    # Update docid in the renamed JSON file
                    data['docid'] = docid
                    with open(new_json_path, 'w') as updated_json_file:
                        json.dump(data, updated_json_file, indent=4)
                    
                    new_ipynb_file = docid + '.ipynb'
                    new_ipynb_path = os.path.join(self.folder_path, new_ipynb_file)
                    os.rename(ipynb_path, new_ipynb_path)
                    print(f"{ipynb_path} --> {new_ipynb_path}")

    def delete_other_files(self):
        for file_name in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, file_name)
            if not (file_name.endswith('.json') or file_name.endswith('.ipynb')):
                os.remove(file_path)
    
    def rename_files_in_folder(self):
        self.collect_file_pairs()
        self.rename_files()
        # self.delete_other_files()


# Usage example
'''
python -m crawler.change_filenames
'''
folder_path = './data/notebook/Kaggle/raw_notebooks'
renamer = FileRenamer(folder_path)
renamer.rename_files_in_folder()

