''' online_resource_management.py
Manage the indexes to be servered online
'''

from utils import utils
from utils import es_tools
import datetime

es = utils.create_es_client()


def switch_to_index(resource_type=None, new_indices=None):
    ''' Change the resource to be served 
    '''
    if resource_type=='notebook' or resource_type=='dataset': 
        for index_name in new_indices: 
            es_tools.update_alias(index_name, f'{resource_type}_online')
        print(f"Serving {resource_type} from [{new_indices}]. ")
        
        current_date = str(datetime.date.today())
        with open('indexing_logs', 'a') as f: 
            f.write(f"{current_date}\t{resource_type}\t{new_indices}\n")

    else: 
        print('Resource type not supported')

def main():
    # switch_to_index(resource_type='notebook', new_indices=['kaggle_notebooks_2023-09-18'])
    switch_to_index(resource_type='dataset', new_indices=['kaggle_datasets_2023-09-25', 'zenodo_datasets_2023-09-25'])


if __name__ == '__main__': 
    # cd search_engine_app
    # python -m management.index_switching
    main()
 