''' online_resource_management.py
Manage the indexes to be servered online
'''

from utils import utils
from utils import es_tools
es = utils.create_es_client()


def switch_to_index(resource_type=None, new_index_name=None):
    ''' Change the resource to be served 
    '''
    if resource_type=='notebook': 
        es_tools.update_alias(new_index_name, f'{resource_type}_online')
        print(f"The system is now serving from [{new_index_name}]. ")

    else: 
        print('Resource type not supported')

def main():
    switch_to_index(resource_type='notebook', new_index_name='kaggle_notebooks_2023-09-18')


if __name__ == '__main__': 
    main()
 