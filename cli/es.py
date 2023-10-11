import argparse
from utils import es_tools

def main():
    parser = argparse.ArgumentParser(description='Elasticsearch Index Operations')
    parser.add_argument('-l', '--list', action='store_true', help='List all indexes')
    parser.add_argument('-d', '--delete', nargs='+', help='Delete indexes (provide index names)')
    parser.add_argument('-u', '--update', nargs=2, help='Update alias (provide index name and alias)')
    parser.add_argument('-g', '--get-docs', nargs='+', help='Get document count for indexes (provide index names)')

    args = parser.parse_args()

    print('================ Elasticsearch Output Start ===============')

    if args.list:
        es_tools.list_indexes()

    if args.delete:
        es_tools.delete_indexes(args.delete)

    if args.update:
        es_tools.update_alias(args.update[0], args.update[1])

    if args.get_docs:
        for index in args.get_docs:
            es_tools.get_doc_number(index)

    print('================ Elasticsearch Output End ===============')

if __name__ == '__main__': 
    main()