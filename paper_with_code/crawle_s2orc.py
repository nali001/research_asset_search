import wget
import os
import json
import ast
import requests

api_key = open(".semantic_scholar_key").read().strip()
os.makedirs('s2orc', exist_ok=True)

r3 = requests.get('https://api.semanticscholar.org/datasets/v1/release/latest/dataset/s2orc', headers={'x-api-key':api_key}).json()

files_links = {}
for f in r3['files']:
    file_name = os.path.basename(f.split('?')[0])
    files_links[file_name] = f

file_names = list(files_links.keys())
for file_name in file_names:
        link = files_links[file_name]
        print(file_name)
        if os.path.exists(os.path.join('s2orc', file_name)):
            continue
        wget.download(link, out='s2orc')

        files_links.pop(file_name)


        # update the file link since links will expire after some time
        r3 = requests.get('https://api.semanticscholar.org/datasets/v1/release/latest/dataset/s2orc', headers={'x-api-key':api_key}).json()

        for f in r3['files']:
            file_name = os.path.basename(f.split('?')[0])
            if file_name in files_links:                
                files_links[file_name] = f