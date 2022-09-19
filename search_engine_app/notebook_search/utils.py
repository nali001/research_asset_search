from elasticsearch import Elasticsearch
ELASTICSEARCH_HOSTNAMES = ["elasticsearch", "localhost"]
def create_es_client() -> Elasticsearch:
    """ Create an Elasticsearch client based on the IP addresses/hostname. 

    In development, it is "localhost"; 
    In deployment, it is "elasticsearch". 

    Returns: 
        es: a elasticsearch client. 

    """
    # Try different host names for Elasticsearch service. 
    # It depends on on what machine the service is running. 
    for host in ELASTICSEARCH_HOSTNAMES: 
        es = Elasticsearch(
            hosts=[{"host": host, "port": 9200}],
            http_auth=["elastic", "changeme"],
            tim_out=30
            )
        if es.ping(): 
            break
    return es

def extract_queries(request): 
    ''' Extract queries from the request. 
    
    '''