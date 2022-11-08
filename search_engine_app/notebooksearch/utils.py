import os

from elasticsearch import Elasticsearch

elasticsearch_hostname = os.environ.get('ELASTICSEARCH_HOSTNAME')
elasticsearch_port = os.environ.get('ELASTICSEARCH_PORT')
elasticsearch_username = os.environ.get('ELASTICSEARCH_USERNAME')
elasticsearch_password = os.environ.get('ELASTICSEARCH_PASSWORD')


def create_es_client() -> Elasticsearch:
    """ Create an Elasticsearch client based on the IP addresses/hostname.
    Returns: 
        es: an elasticsearch client.

    """
    valid_es = None
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
