# Data collection pipeline
## Dataset collection
The dataset crawling is simple, so one script can support multiple dataset respositories
1. `crawler/dataset/dataset_crawling.py`
    - metadata file: file_name <-- 'DS_' + Hash(identifier).json

2. `preprocessor/dataset/preprocessing.py`
    - mapping metadata

3. `indexer/dataset_bulk_indexing.py`
    - Gnerate an index in Elasticsearch as `{source_name.lower()}_datasets_{current_date}`

4. `search_engine_app/management/index_switching.py`
    - Add indexes names to `.env` 

## Computational notebook collection
The computational notebook crawling need to be customized to each repositories. 
+ 1. From GitHub: `crawler/notebooks/github_crawler/notebook_crawling.py`
    - source file: file_name <-- 'NB_' + Hash(identifier) + '.ipynb'
    - metadata file: file_name <-- 'NB_' + Hash(identifier) + '.json'
    - nb['docid'] <-- 'NB_' + Hash(identifier)

+ 2. 
