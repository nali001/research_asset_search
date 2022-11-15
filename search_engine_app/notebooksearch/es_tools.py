from notebooksearch import utils
es = utils.create_es_client()

def list_indexes():
    print(f'---------- Indexes ----------')
    indexes = es.indices.get_alias("*")
    for i in indexes: 
        print(i)

def get_doc_number(index_name):
    es.indices.refresh(index=index_name)
    result = es.cat.count(index=index_name, params={"format": "json"})
    print(f'---------- # doc of `{index_name}` ----------')
    print(f'{result[0]["count"]}\n')

def main():
    get_doc_number('kaggle_raw_notebooks')

if __name__ == '__main__': 
    main()