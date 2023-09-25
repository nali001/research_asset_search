# Field mappings
# `docid`, `source` and `size` are generated with scripts. Others are directly mapped. 
UNIFIED_METADATA_SCHEMA = {
    "docid": None,
    "size": None, 
    "name": None,
    "description": None,
    "html_url": None,
    "source": None,
    "source_id": None,
    "last_updated": None, 
    "license": None, 
}



ZENODO_MATADATA_MAPPING = {
    "docid": ['docid'], 
    "source": ['source'],
    "size": ['size'], 
    "name": [('metadata', 'title')],
    "description": [('metadata', 'title'), ('metadata', 'description'), ('metadata', 'keywords')],
    "html_url": [('links', 'html')],
    "source_id": ['doi'],
    "last_updated": ['updated'], 
    "license": [('metadata', 'license', 'id')], 
}

KAGGLE_METADATA_MAPPING = {
    "docid": ['docid'],
    "source": ['source'],
    "size": ['size'], 
    "name": ['title'],
    "description": ['title', 'subtitile', 'description'],
    "html_url": ['url'],
    "source_id": ['ref'],
    "last_updated": ['lastUpdated'], 
    "license": ['licenseName'], 
}



DRYAD_CONTENT_MAPPING = {
    "docid": ['docid'],
    "source": ['source'],
    "size": ['size'], 
    "name": ['title'],
    "description": ['abstract'],
    "html_url": ['sharingLink'],
    "source_id": ['identifier'],
    "last_updated": ['lastModificationDate'], 
    "license": ['license'],
}


