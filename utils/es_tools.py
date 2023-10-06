from utils import utils
es = utils.create_es_client()

def list_indexes():
    print(f'---------- Indexes ----------')
    indexes = es.indices.get_alias(index="*")
    for i in indexes: 
        print(i)

def update_alias(index, alias):
    if es.indices.exists_alias(alias): 
        es.indices.delete_alias('_all', alias)
    es.indices.put_alias(index=index, name=alias)
    print(f'Add name [{alias}] to index [{index}]')


def get_doc_number(index_name):
    es.indices.refresh(index=index_name)
    result = es.cat.count(index=index_name, params={"format": "json"})
    print(f'---------- # doc of `{index_name}` ----------')
    print(f'{result[0]["count"]}\n')

def main():
    print('================ Elasticsearch Output Start ===============')
    list_indexes()
    # print(es.indices.get_alias(index='notebook_online'))
    # print(es.indices.get_alias(index='dataset_online'))
    # get_doc_number('kaggle_raw_notebooks')
    # get_doc_number('kaggle_raw_notebooks')
    # get_doc_number('kaggle_notebook_summarization')
    # update_alias('kaggle_notebook_summarization', 'kaggle_online')
    # list_indexes()
    print('================ Elasticsearch Output End ===============')



if __name__ == '__main__': 
    main()
    