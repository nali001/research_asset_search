# Data collection pipeline
## Dataset collection
1. `crawler/dataset/dataset_crawling.py`
    - metadata file: file_name <-- 'DS_' + Hash(identifier).json
2. `preprocessor/dataset/preprocessing.py`
    - mapping metadata

3. `indexer/dataset_indexing.py`

## Computational notebook collection
+ 1. `crawler/notebooks/github_crawler/notebook_crawling.py`
    - source file: file_name <-- 'NB_' + Hash(identifier) + '.ipynb'
    - metadata file: file_name <-- 'NB_' + Hash(identifier) + '.json'
    - nb['docid'] <-- 'NB_' + Hash(identifier)

+ 2. 
