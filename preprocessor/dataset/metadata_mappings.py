# Field mappings
# `docid`, `source` and `size` are generated with scripts. Others are directly mapped. 
UNIFIED_METADATA_SCHEMA = {
    "docid": None,
    "source": None,
    "size": None, 
    "name": None,
    "description": None,
    "html_url": None,
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
    # "last_updated": ['updated'], 
    "last_updated": ['last_updated'], 
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
    # "last_updated": ['lastUpdated'], 
    "last_updated": ['last_updated'], 
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
    # "last_updated": ['lastModificationDate'], 
    "last_updated": ['last_updated'], 
    "license": ['license'], 
}

DRYAD_LICENSES = {
    "https://creativecommons.org/publicdomain/zero/1.0/": "CC0 1.0 Universal", 
}

