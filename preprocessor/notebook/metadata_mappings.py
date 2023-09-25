# Field mappings
# ---------------- Schema -----------------
UNIFIED_MATADATA_SCHEMA = {
    "docid": None,
    "source_id": None,
    "stargazers_count": None,
    "forks_count": None,
    "size": None,
    "name": None,
    "html_url": None,
    "git_url": None,
    "source": None,
    "code_file": None,
    "description": None,
    "language": None,
    "num_cells": None,
    "num_code_cells": None,
    "num_md_cells": None,
    "len_md_text": None
}

# ---------------- Map from metadata -----------------
GITHUB_MATADATA_MAPPING = {
    'docid': ['docid'], 
    'source_id': ['git_url'], 
    "stargazers_count": [], 
    "forks_count": [], 
    'size': ['size'],
    'name': [], 
    'html_url': ['html_url'],
    'git_url': ['git_url'], 
    'source': [], 
    'code_file': ['name'], 
}

KAGGLE_METADATA_MAPPING = {
    'docid': ['docid'], 
    'source_id': ['id'], 
    "stargazers_count": [], 
    "forks_count": [], 
    'size': [],
    'name': ['title'],
    'html_url': ['html_url'], 
    'git_url': [], 
    'source': [], 
    'code_file': ['code_file'], 
}

# ---------------- Extract from contents -----------------
COMMON_CONTENT_MAPPING = {
    'docid': ['docid'], 
    'description': ['md_text_clean'],
    'html_url': ['html_url'],
    'language': ['language'],
    'num_cells': ['num_cells'],
    'num_code_cells': ['num_code_cells'],
    'num_md_cells': ['num_md_cells'],
    'len_md_text': ['len_md_text']
}


GITHUB_CONTENT_MAPPING = {
    'docid': ['docid'],
    'name': ['title'],
    'description': ['description'],
    'language': ['language'],
    'num_cells': ['num_cells'],
    'num_code_cells': ['num_code_cells'],
    'num_md_cells': ['num_md_cells'],
    'len_md_text': ['len_md_text'],
    'summarization_t5': ['summarization_t5'],
    'summarization_relevance': ['summarization_relevance'],
    'summarization_confidence': ['summarization_confidence']
}

KAGGLE_CONTENT_MAPPING = {
    'docid': ['docid'], 
    'description': ['description'], 
    'language': ['language'],
    'num_cells': ['num_cells'],
    'num_code_cells': ['num_code_cells'],
    'num_md_cells': ['num_md_cells'],
    'len_md_text': ['len_md_text'],
    'summarization_t5': ['summarization_t5'],
    'summarization_relevance': ['summarization_relevance'],
    'summarization_confidence': ['summarization_confidence']
}
