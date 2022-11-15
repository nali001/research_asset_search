import os
import json 
from elasticsearch import Elasticsearch

def read_json_file(file):
    read_path = file
    with open(read_path, "r", errors='ignore') as read_file:
        data = json.load(read_file)
    return data


def create_es_client() -> Elasticsearch:
    """ Create an Elasticsearch client based on the IP addresses/hostname.
    Returns: 
        es: an elasticsearch client.

    """
    valid_es = None
    elasticsearch_hostname = os.environ.get('ELASTICSEARCH_HOSTNAME')
    elasticsearch_port = os.environ.get('ELASTICSEARCH_PORT')
    elasticsearch_username = os.environ.get('ELASTICSEARCH_USERNAME')
    elasticsearch_password = os.environ.get('ELASTICSEARCH_PASSWORD')
    print(f'\n\nelasticsearch_hostname: {elasticsearch_hostname}\n\n\n')
    
    es = Elasticsearch(
        hosts=[{"host": elasticsearch_hostname, "port": elasticsearch_port}],
        http_auth=[elasticsearch_username, elasticsearch_password],
        tim_out=30
    )
    if es.ping():
        print(f'\nVALID ELASTICSEARCHHHHHHHHHH: {elasticsearch_hostname}\n')
        valid_es = es
    if valid_es == None:
        print(f'\n\nElasticsearch is NOT ready yet!\n\n')
        # If there is no connection.
    return valid_es
